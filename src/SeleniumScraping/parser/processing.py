"""Prepare data for export."""

# Future Implementations
from __future__ import annotations

# Standard Library
import ssl

from html import unescape
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from zipfile import ZIP_DEFLATED, ZipFile

# Thirdparty Library
import numpy as np
import pandas as pd
import regex as re

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3
from geopy.location import Location
from tqdm import tqdm

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.records import RecordsData
from SeleniumScraping.driver.utils import (
    all_str,
    print_method,
    print_method_success,
)
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.parser.utils import (
    ProcessDate,
    normalize_str,
    replace_whitespace,
)


re.DEFAULT_VERSION = re.V1


class Processing(RecordsData):
    """Data processing."""

    def __init__(self, driver: TorBrowser):
        self.variable_labels = {
            "query": "Address or Place that was given to GoogleMaps",
            "address": "Address or Place that GoogleMaps found for the given query",
            "lat": "Latitude of the found GoogleMaps address",
            "lng": "Longitude of the found GoogleMaps address",
            "alt": "Altitude of the found GoogleMaps address",
        }
        self.pat_m = re.compile("Male")
        self.pat_f = re.compile("Female")
        self.put_u = re.compile("Unknown")
        self.pat_num = re.compile(r"\d+")
        self.pat_only_num = re.compile(r"^\d+$")
        self.pat_month = re.compile(r"\d+m")
        self.pat_day = re.compile(r"\dd")
        self.pat_hour = re.compile(r"\dh")
        self.driver = driver
        self.pat_mar = re.compile("^M$")
        self.pat_wid = re.compile("^W$")
        self.to_pat = re.compile(r"(?<=\s)(to\s)")
        self.from_pat = re.compile(r"^(from\s)")
        self.about_after_pat = re.compile(r"^(after||about)")
        self.pat_mis = re.compile(
            r"((?<![A-z])\,\s,(?=\s))|(\s\,(?=\s))|(^\,\s)"
        )
        self.split_pat = re.compile(r"\,\s", flags=re.REVERSE)

        self.process_date = ProcessDate()

        self.get_coords = Coords(driver)
        super().__init__(driver)

    def reorder_columns(self, df_: pd.DataFrame) -> pd.DataFrame:
        """Reorder the final DataFrame in a convenient way.

        Parameters
        ----------
        df_ : pd.DataFrame
            DataFrame for which the order of the columns should be changed.

        Returns
        -------
        df_intended_order : pd.DataFrame
            Supplied DataFrame with reordered columns.
        """
        geo_cols_list = ["query", "address", "lat", "lng"]

        geo_cols_set = set(geo_cols_list)

        df_alph_order = df_[sorted(df_.columns.to_list())]

        all_cols = set(df_alph_order.columns.to_list())

        all_cols.symmetric_difference_update(geo_cols_set)

        new_col_order = list(geo_cols_list) + list(all_cols)

        df_intended_order = df_alph_order[new_col_order]

        return df_intended_order

    def columns_create(
        self, records_data: pd.DataFrame, records_name: str
    ) -> pd.DataFrame:
        """Apply common scheme to the birth, death and burial columns."""
        process_date = ProcessDate()

        records_copy = records_data.copy(deep=True)

        column_date = "_".join([records_name, "date"])
        column_place = "_".join([records_name, "place"])

        # Extract column of interest from DataFrame and rename it to `column_place`.
        records_split = records_copy[[records_name]].rename(
            columns={records_name: column_place}
        )

        # Extract the date from `column_place` and put the extracted date into its own column.
        records_split[column_date] = [
            process_date.extract_date(str_)
            for str_ in records_split[column_place]
        ]

        # Format the date from `column_date`.
        records_split[column_date] = [
            process_date.format_date(str_)
            for str_ in records_split[column_date]
        ]

        # Remove the date from column `column_place`.
        records_split[column_place] = [
            process_date.remove_date(str_)
            for str_ in records_split[column_place]
        ]

        # Remove leading or trailing commas.
        records_split[column_place] = [
            self.pat_mis.sub("", str_).strip()
            for str_ in records_split[column_place]
        ]

        return records_split

    def get_strl_cols(self, df_: pd.DataFrame) -> list[str]:
        """Return list of strl columns.

        List of columns to store in Statas "strl" format in order to make
        the Stata dataset smaller.

        Parameters
        ----------
        df_ : pd.DataFrame
            DataFrame for which to return the strl columns.

        Returns
        -------
        strl_cols : list
            Columns which can be specified as Stata strl columns.
        """
        strl_idx = np.where(
            ("O" == df_.dtypes).values * (~df_.columns.str.endswith("date"))
        )[0]

        strl_cols = df_.iloc[:, strl_idx].columns.to_list()

        return strl_cols

    def convert_dates(self, df_: pd.DataFrame):
        """Return dict with date columns for the Stata export.

        Parameters
        ----------
        df_ : pd.DataFrame
            Columns for which to create the date dict..

        Returns
        -------
        dict
            Dict object with the name of the date columns as keys and 'td' as
            values.
        """
        return {x: "td" for x in set(df_.filter(regex=(".*_date")).columns)}

    def drop_empty_cols(self, df_: pd.DataFrame) -> pd.DataFrame:
        """Remove empty columns.

        Parameters
        ----------
        df_ : pd.DataFrame
            DataFrame for which empty columns should be removed.

        Returns
        -------
        pd.DataFrame
             Input DataFrame with empty columns removed.
        """
        # Check whether one of the date columns is empty. NOTE: This is
        # necessary because if one of the date columns should be empty then it
        # will not have the required stata format and thus will
        df_idx = df_.apply(lambda x: not x.unique().size == 1).pipe(np.where)[
            0
        ]

        return df_.iloc[:, df_idx]

    def add_coords(self, records_df: pd.DataFrame) -> pd.DataFrame:
        """Apply geocoding to the currently active country records."""
        print_method(
            "add_coords", "I will try to geocode the requested records..."
        )
        # `death_registration_place` usually contains the most accurate
        # information about the place. Missing `death_registration_place`
        # should be replaced with `burial_place` as `burial_place` usually
        # contains the second most accurate information. Should both
        # `death_registration_place` and `burial_place` be missing then
        # missing entries should be replaced with `death_place`.

        records_places = records_df.copy(deep=True).filter(regex="place")

        records_places["place"] = records_places.apply(
            lambda row: row["death_registration_place"]
            if row["death_registration_place"] != ""
            else row["burial_place"]
            if row["burial_place"] != ""
            else row["death_place"],
            axis=1,
        )

        # Split `records_places` into its four components: country,
        # municipality, city and church. Fill missing entries with "" after
        # the concatenation.  Rename the columns of splitted DataFrame.
        # Renaming the columns seperately has the advantage that missing
        # columns will should be ignored instead of raising an error.  The
        # church column can be dropped as the city coordinates should be
        # sufficient and are also easier to geocode.
        place_record_split = (
            pd.DataFrame(
                data=[
                    self.split_pat.split(str_)
                    for str_ in records_places["place"]
                ]
            )
            .fillna("")
            .rename(
                columns={
                    0: "country",
                    1: "municipality",
                    2: "city",
                    3: "church",
                },
            )
            .drop(columns=["church"], errors="ignore")
        )

        for pat_ in [self.to_pat, self.from_pat, self.about_after_pat]:

            place_record_split = place_record_split.apply(
                lambda x: [pat_.sub("", str_) for str_ in x]
            )

        i = 0
        while i < 2:
            place_record_split = place_record_split.apply(
                lambda x: [self.process_date.remove_date(str_) for str_ in x]
            )
            i += 1

        # Sort values
        place_record_split.sort_values(
            by=["country", "municipality", "city"], inplace=True
        )

        # DataFrame using the same value order as was used for
        # `place_record_split`.
        records_df_sorted = records_df.iloc[place_record_split.index]

        # Reset index of sorted copy of the original DataFrame.
        records_df_sorted.reset_index(drop=True, inplace=True)

        # Create copy of `place_record_split` and reset the index for it as
        # well.
        place_record_split_sorted = place_record_split.reset_index(drop=True)

        # Remove duplicated entries from the sorted copy of
        # `place_record_split`.
        places_unique = place_record_split_sorted.drop_duplicates()

        # Series where each row is equal to one API request to the GoogleMaps
        # API.
        query_series = (
            places_unique["city"]
            + ", "
            + places_unique["municipality"]
            + ", "
            + places_unique["country"]
        )

        # Remove leading and trailing commas from the query Series.
        query_series = pd.Series(
            [self.pat_mis.sub("", str_).strip() for str_ in query_series]
        )

        # Remove empty rows from the query Seris. NOTE: this step is very
        # important because an API request to GoogleMaps with an empty string
        # will lead to an error with, unfortunately, a very confusing error
        # message.
        query_series = query_series.iloc[
            np.where(query_series != "")[0].tolist()
        ]

        # Drop duplicates again from the query Series just to be sure.
        query_series.drop_duplicates(inplace=True)

        # Remove the same elements from `places_unique` that were previously
        # also removed from `query_series`. NOTE: this step is very important
        # because otherwise `query_series` and `places_unique` will be of
        # different length leading to an index error.
        places_unique = places_unique.iloc[query_series.index]

        # Start the geocoding using the query Series.
        geo_pd = self.get_coords(query_series).set_index(places_unique.index)

        # Add the found latitue and longitudes to the original DataFrame.
        records_final = pd.concat(
            [records_df_sorted, geo_pd], axis=1, join="outer"
        )

        # Replace missing coordinates with the last non-missing observation.
        records_final[geo_pd.columns.to_list()] = records_final[
            geo_pd.columns.to_list()
        ].ffill()

        print_method_success(
            "add_coords", "I succesfully geocoded the requested records!"
        )

        return records_final

    def __call__(self, country: Optional[str] = None) -> pd.DataFrame:
        """Export collected data."""
        print_method(
            "Processing.__call__",
            "I will try to export the records to Stata...",
        )
        if country is not None:
            self.event_country = country

        records_path = Path(self.load_records())

        # Loading the records data
        records_df: pd.DataFrame = (
            pd.read_feather(records_path)
            .reset_index(drop=True)
            .fillna("")
            .apply(replace_whitespace)
            .apply(normalize_str)
            .apply(lambda x: [unescape(df_row) for df_row in x])
        )

        # ------------------------------------------------------------------ #
        #                Seperate event_date from event_place                #
        # ------------------------------------------------------------------ #
        column_list: list[pd.DataFrame] = []

        create_col_names = [
            "birth",
            "death",
            "death_registration",
            "burial",
            "christening",
        ]

        for l_name in create_col_names:
            try:
                column_list.append(self.columns_create(records_df, l_name))
            except KeyError:
                # Create missing column if it should not exist
                column_list.append(
                    pd.DataFrame(
                        data=[""] * len(records_df),
                        index=records_df.index,
                        columns=["_".join([l_name, "place"])],
                    )
                )

        # Append main dataframe to the list of columns
        column_list.append(records_df)

        # Concatenate newly created columns
        records_df = (
            pd.concat(column_list, axis=1)
            # .fillna("")
            .drop(
                columns=create_col_names,
                errors="ignore",
            )
        )

        # Add coordinates to the DataFrame.
        records_df = self.add_coords(records_df)

        # ------------------------------------------------------------------ #
        #                        Adjust marital values                       #
        # ------------------------------------------------------------------ #

        if "marital_status" in set(records_df.columns):

            # Replace "marital_status" with "Married" if "marital_status" is
            # "M"
            records_df["marital_status"] = [
                self.pat_mar.sub(str_, "Married")
                if bool(self.pat_mar.search(str_))
                else str_
                for str_ in records_df["marital_status"]
            ]

            # Replace "marital_status" with "Widowed" if "marital_status" is
            # "W"
            records_df["marital_status"] = [
                self.pat_wid.sub(str_, "Widowed")
                if bool(self.pat_wid.search(str_))
                else str_
                for str_ in records_df["marital_status"]
            ]

        # ------------------------------------------------------------------ #
        #                        Adjust gender values                        #
        # ------------------------------------------------------------------ #

        # TODO: Check if there were values other than "Male", "Female" or
        # "Unknown" that were part of the "gender" or "sex" column.

        if "sex" in set(records_df.columns):
            records_df["sex"] = [
                0
                if bool(self.pat_m.search(str_))
                else 1
                if bool(self.pat_f.search(str_))
                else np.nan
                if bool(self.put_u.search(str_))
                else np.nan
                for str_ in records_df["sex"]
            ]

            records_df.rename(columns={"sex": "female"}, inplace=True)

        # ------------------------------------------------------------------ #
        #                        Adjusting age values                        #
        # ------------------------------------------------------------------ #

        if "age" in set(records_df.columns):
            records_df["age"] = [
                round(int(self.pat_num.findall(str_)[0]) / (24 * 365), 6)
                if bool(self.pat_hour.search(str_))
                else round(int(self.pat_num.findall(str_)[0]) / 365, 6)
                if bool(self.pat_day.search(str_))
                else round(int(self.pat_num.findall(str_)[0]) / 12, 6)
                if bool(self.pat_month.search(str_))
                else np.nan
                if str_ == ""
                else float(str_)
                if bool(self.pat_only_num.search(str_))
                else np.nan
                for str_ in records_df["age"]
            ]

            records_df["age"] = records_df["age"].astype(float)

        records_df.rename(columns={"ethnicity": "nationality"}, inplace=True)

        # Check whether one of the date columns is empty. NOTE: This is
        # necessary because if one of the date columns should be empty then it
        # will not have the required stata format and thus will
        records_df = self.drop_empty_cols(records_df)

        # Reorder columns
        records_df = self.reorder_columns(records_df)

        # Remove any duplicated columns that could appear
        records_df = records_df.loc[:, ~records_df.columns.duplicated()]

        # List containing the names of all string columns.
        str_cols = self.get_strl_cols(records_df)

        # NOTE: When using the `convert_strl` keyword of the `to_stata` method
        # it is very important to make sure that all of the columns listed in
        # the `convert_strl` keyword do not contain any elements that could be
        # interpreted as something other than type str! Otherwise the very
        # unhelpful TypeError "encoding without a string argument" is raised
        # which basically means just that: one of the columns listed in
        # `convert_strl` contains a row with a value that could be interpreted
        # as a float or something else than a string. A simple trick to avoid
        # this exception is simply to use the `fillna("")` method with an
        # empty string as an argument.
        records_df.loc[:, str_cols] = records_df[str_cols].fillna("")

        with TemporaryDirectory() as temp_dir:

            # Filepath for resulting, non temporary zip file.
            export_path = (
                FilePaths.export_dir_user_path
                / records_path.name.replace(".feather", ".zip")
            )

            # Filepath for the for the file inside the temporary folder.
            temp_filename = Path(temp_dir) / records_path.name.replace(
                ".feather", ".dta"
            )

            # Filename for the `arcname` argument of `ZipFile.write()`. For
            # the `arcname` the same argument input should be used as was used
            # for the previous argument `filename` but without the filepath,
            # so basically should the filename part of the `filename`
            # argument. It is necessary/important to specify the `arcname`
            # argument because otherwise the resulting zipfile will not only
            # contain the Stata-file but will also replicate the complete
            # folder structure of the input file which leads to a lot of
            # unncessary folders.
            temp_arcname = temp_filename.name

            # Export data in Stata format
            records_df.to_stata(
                temp_filename,
                variable_labels=self.variable_labels,
                convert_dates=self.convert_dates(records_df),
                write_index=False,
                convert_strl=self.get_strl_cols(records_df),
                data_label="Familysearch Data",
                version=117,
            )

            with ZipFile(export_path, "w", ZIP_DEFLATED) as zip_:
                zip_.write(filename=temp_filename, arcname=temp_arcname)

        print_method_success(
            "Processing.__call__",
            "I successfully exported the records to Stata!",
        )

        return records_df


class Coords(RecordsData):
    """Retrieve coordinates from googlemaps."""

    # Enable the pandas package to show a progressbar while geocoding records.
    tqdm.pandas()

    def __init__(self, driver: TorBrowser) -> None:
        # Disable certificate checking for the GoogleMaps API requests.
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Create a geolocator method using the GoogleMaps API key that can
        # be called to geocode the provided string. NOTE: the default timeout
        # is usually far too short and thus restrictive and should be set to at
        # least 20 seconds or even longer.
        geolocator = GoogleV3(
            api_key=FilePaths.google_key, timeout=20, ssl_context=ctx
        )

        # Restrict the geolocator to one request per second and retry requests
        # up to 5 times.
        self.geocode = RateLimiter(
            geolocator.geocode, min_delay_seconds=1, max_retries=5
        )

        self.driver = driver
        super().__init__(driver)

    def get_features(self, geo: Location) -> list[str | float | None]:
        """Extract and return the features from the supplied Location object.

        Parameters
        ----------
        geo : Location
            Location object holding the GoogleMaps features.

        Returns
        -------
        list of str or float or None
            List containing either the address as string and the latitude,
            longitude and altitude as float in that order or, in case that
            the supplied Location should be empty, a list of length 5
            only containing NoneType objects.
        """
        if geo is None:
            return [np.nan, np.nan, np.nan, np.nan]

        return [geo.address, geo.latitude, geo.longitude, geo.altitude]

    def __call__(self, query_series: pd.Series) -> pd.DataFrame:
        """Geocode the supplied query Series.

        Parameters
        ----------
        query_series : pd.Series
            Series containing the query strings that will be sent to the
            GoogleMaps API.

        Returns
        -------
        return_pd : pd.DataFrame
            DataFrame containing the supplied queries together with the found
            coordinates.
        """
        assert isinstance(query_series, pd.Series)

        assert all_str(query_series)

        assert isinstance(self.event_country, str)

        # Path to DataFrame containing already conducted geocoding for the
        # current country.
        query_path = (
            FilePaths.query_dir
            / f"{self.event_country.lower()}_records_query.feather"
        )

        # Test whether geocoding history exists.
        if query_path.exists():
            print(f"I found a geocoding history for {self.event_country}!")
            orig_query_pd = pd.read_feather(query_path)

            # Locations that have not already been geocoded, thus strings not
            # part of the query DataFrame.
            query_miss_index = np.where(
                ~query_series.isin(orig_query_pd["query"])
            )[0]

        # Start geocoding if either not all entries of the given query Series
        # are part of the geocoding history or if the geocoding does not
        # exist.
        if not query_path.exists() or len(query_miss_index) >= 1:  # type: ignore

            # If a geocoding history already exists then subset the query
            # Series to only include elements that have not already been
            # geocoded.
            if query_path.exists():
                geo_pd = pd.DataFrame(
                    query_series.iloc[query_miss_index], columns=["query"]  # type: ignore
                )
            else:
                geo_pd = pd.DataFrame(query_series, columns=["query"])

            geo_pd["location"] = geo_pd["query"].progress_apply(self.geocode)

            rename_dict = {0: "address", 1: "lat", 2: "lng", 3: "alt"}

            new_query_pd = pd.DataFrame(
                data=[self.get_features(str_) for str_ in geo_pd["location"]]
            ).rename(columns=rename_dict)

            new_query_pd["query"] = geo_pd["query"].to_list()

            new_query_pd = new_query_pd[
                ["query"] + list(rename_dict.values())
            ].reset_index(drop=True)

            if "orig_query_pd" in locals():
                orig_query_pd = orig_query_pd.append(new_query_pd)  # type: ignore
            else:
                orig_query_pd = new_query_pd

            orig_query_pd.reset_index(drop=True, inplace=True)
            orig_query_pd.to_feather(query_path)

        query_pd = pd.DataFrame(query_series, columns=["query"])

        orig_query_pd_mod = orig_query_pd.set_index(keys=["query"], drop=True)  # type: ignore

        # NOTE: It's important to know that when when joining on the index
        # (default) the resulting DataFrame will inherit the index not of the
        # original DataFrame but the index of the joining DataFrame. To use
        # the index of the original DataFrame the "on" keyword of "join" must
        # be used.
        return_pd = query_pd.join(orig_query_pd_mod, how="inner", on="query")

        return_pd.drop_duplicates(inplace=True)

        return return_pd


def parser_records_export(country: str):
    """Export records driver using the command line."""
    driver = TorBrowser(dev_mode=True)
    export_data = Processing(driver)

    export_data(country)

    driver.close_browser()
