"""Scrape familysearch."""

# Future Implementations
from __future__ import annotations

# Standard Library
import ssl

from typing import List, Union

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
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.parser.utils import (
    ProcessDate,
    columns_create,
    normalize_str,
    replace_whitespace,
)


re.DEFAULT_VERSION = re.V1


class Coords(RecordsData):
    """Retrieve coordinates from googlemaps."""

    tqdm.pandas()

    def __init__(self, driver: TorBrowser) -> None:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        geolocator = GoogleV3(
            api_key=FilePaths.google_key, timeout=20, ssl_context=ctx
        )
        self.geocode = RateLimiter(
            geolocator.geocode, min_delay_seconds=1, max_retries=5
        )

        self.driver = driver
        super().__init__(driver)

    def get_features(self, geo: Location) -> List[Union[str, float, None]]:
        """Get features from geodata."""
        if geo is None:
            return [np.nan, np.nan, np.nan, np.nan]

        return [geo.address, geo.latitude, geo.longitude, geo.altitude]

    def __call__(self, query_series: pd.Series) -> pd.DataFrame:
        """Use GoogleMaps to determine longitude and latitude of record
        entry."""
        assert isinstance(query_series, pd.Series)

        assert all([isinstance(str_, str) for str_ in query_series])

        # Path to DataFrame containing already conducted geocoding for the current country.
        query_path = (
            FilePaths.query_dir
            / f"{self.event_country.lower()}_records_query.feather"
        )

        # Test whether geocoding history exists.
        if query_path.exists():
            print(f"I found a geocoding history for {self.event_country}!")
            orig_query_pd = pd.read_feather(query_path)

            # Locations that have not already been geocoded, thus strings not part of the query DataFrame.
            query_miss_index = np.where(
                ~query_series.isin(orig_query_pd["query"])
            )[0]

        # Start geocoding if either not all entries of the given query Series
        # are part of the geocoding history or if the geocoding does not exist.
        if not query_path.exists() or len(query_miss_index) >= 1:

            # If a geocoding history already exists then subset the query Series
            # to only include elements that have not already been geocoded.
            if query_path.exists():
                geo_pd = pd.DataFrame(
                    query_series.iloc[query_miss_index], columns=["query"]
                )
            else:
                geo_pd = pd.DataFrame(query_series, columns=["query"])

            geo_pd["location"] = geo_pd["query"].progress_apply(self.geocode)

            rename_dict = dict({0: "address", 1: "lat", 2: "lng", 3: "alt"})

            new_query_pd = pd.DataFrame(
                data=[self.get_features(str_) for str_ in geo_pd["location"]]
            ).rename(columns=rename_dict)

            new_query_pd["query"] = geo_pd["query"].to_list()

            new_query_pd = new_query_pd[
                ["query"] + list(rename_dict.values())
            ].reset_index(drop=True)

            if query_path.exists():
                orig_query_pd = orig_query_pd.append(new_query_pd)
            else:
                orig_query_pd = new_query_pd

            orig_query_pd.reset_index(drop=True, inplace=True)
            orig_query_pd.to_feather(query_path)

        query_pd = pd.DataFrame(query_series, columns=["query"])

        orig_query_pd_mod = orig_query_pd.set_index(keys=["query"], drop=True)

        # NOTE: It's important to know that when when joining on the index (default)
        # the resulting DataFrame will inherit the index not of the original
        # DataFrame but the index of the joining DataFrame. To use the
        # index of the original DataFrame the "on" keyword of "join" must
        # be used.
        return_pd = query_pd.join(orig_query_pd_mod, how="inner", on="query")

        return return_pd


class RecordsGeocode(RecordsData):
    """Geocode Records data."""

    def __init__(self, driver: TorBrowser):

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

    def __call__(self) -> pd.DataFrame:
        """Apply geocoding to the currently active country records."""
        records_path = self.load_records()

        records_df: pd.DataFrame = (
            pd.read_feather(records_path)
            .reset_index(drop=True)
            .fillna("")
            .apply(replace_whitespace)
            .apply(normalize_str)
        )

        # ------------------------------------------------------------------ #
        #                        Extract Place Columns                       #
        # ------------------------------------------------------------------ #

        column_list: List[pd.DataFrame] = []

        try:
            birth_columns = columns_create(records_df, "birth")
            column_list.append(birth_columns)
        except KeyError:
            pass

        try:
            death_columns = columns_create(records_df, "death")
            column_list.append(death_columns)
        except KeyError:
            pass

        try:
            death_registration_columns = columns_create(
                records_df, "death_registration"
            )
            column_list.append(death_registration_columns)
        except KeyError:
            pass

        try:
            burial_columns = columns_create(records_df, "burial")
            column_list.append(burial_columns)
        except KeyError:
            pass

        records_places = (
            pd.concat(column_list, axis=1).filter(regex="place").fillna("")
        )

        # `death_registration_place` usually contains the most accurate
        # information about the place. Missing `death_registration_place`
        # should be replaced with `burial_place` as `burial_place` usually
        # contains the second most accurate information. Should both
        # `death_registration_place` and `burial_place` be missing then
        # missing entries should be replaced with `death_place`.
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
        # the concatenation.
        place_record_split = pd.DataFrame(
            data=[
                self.split_pat.split(str_) for str_ in records_places["place"]
            ]
        ).fillna("")

        # Rename the columns of splitted DataFrame. Renaming the columns
        # seperately has the advantage that missing columns will should be
        # ignored instead of raising an error
        place_record_split.rename(
            columns={0: "country", 1: "municipality", 2: "city", 3: "church"},
            inplace=True,
        )
        # The church column can be dropped as the city coordinates should be
        # sufficient and are also easier to geocode.
        place_record_split.drop(
            columns=["church"], inplace=True, errors="ignore"
        )

        place_record_split["country"] = [
            self.to_pat.sub("", str_) for str_ in place_record_split["country"]
        ]
        place_record_split["municipality"] = [
            self.to_pat.sub("", str_)
            for str_ in place_record_split["municipality"]
        ]
        place_record_split["city"] = [
            self.to_pat.sub("", str_) for str_ in place_record_split["city"]
        ]

        place_record_split["country"] = [
            self.from_pat.sub("", str_)
            for str_ in place_record_split["country"]
        ]
        place_record_split["municipality"] = [
            self.from_pat.sub("", str_)
            for str_ in place_record_split["municipality"]
        ]
        place_record_split["city"] = [
            self.from_pat.sub("", str_) for str_ in place_record_split["city"]
        ]

        place_record_split["country"] = [
            self.about_after_pat.sub("", str_)
            for str_ in place_record_split["country"]
        ]
        place_record_split["municipality"] = [
            self.about_after_pat.sub("", str_)
            for str_ in place_record_split["municipality"]
        ]
        place_record_split["city"] = [
            self.about_after_pat.sub("", str_)
            for str_ in place_record_split["city"]
        ]

        place_record_split["country"] = [
            self.process_date.remove_date(str_)
            for str_ in place_record_split["country"]
        ]
        place_record_split["municipality"] = [
            self.process_date.remove_date(str_)
            for str_ in place_record_split["municipality"]
        ]
        place_record_split["city"] = [
            self.process_date.remove_date(str_)
            for str_ in place_record_split["city"]
        ]

        place_record_split["country"] = [
            self.process_date.remove_date(str_)
            for str_ in place_record_split["country"]
        ]
        place_record_split["municipality"] = [
            self.process_date.remove_date(str_)
            for str_ in place_record_split["municipality"]
        ]
        place_record_split["city"] = [
            self.process_date.remove_date(str_)
            for str_ in place_record_split["city"]
        ]

        # Sort values
        place_record_split.sort_values(
            by=["country", "municipality", "city"], inplace=True
        )

        # Apply sorted index to original DataFrame.
        records_df = records_df.iloc[place_record_split.index]

        records_df.reset_index(drop=True, inplace=True)

        # Reset index of sorted DataFrame as well.
        place_record_split.reset_index(drop=True, inplace=True)

        places_unique = place_record_split.drop_duplicates()

        query_series = (
            places_unique["city"]
            + ", "
            + places_unique["municipality"]
            + ", "
            + places_unique["country"]
        )

        query_series = pd.Series(
            [self.pat_mis.sub("", str_).strip() for str_ in query_series]
        )

        geo_pd = self.get_coords(query_series)

        geo_pd.set_index(places_unique.index, inplace=True)

        records_final = pd.concat([records_df, geo_pd], axis=1, join="outer")

        records_final[geo_pd.columns.to_list()] = records_final[
            geo_pd.columns.to_list()
        ].ffill()

        return records_final
