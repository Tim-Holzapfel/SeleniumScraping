"""Utility functions."""

# Future Implementations
from __future__ import annotations

# Standard Library
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

# Thirdparty Library
import pandas as pd
import pycountry
import regex as re

from shapefile import Reader

# Package Library
from SeleniumScraping.driver.utils import (
    ordinal,
    print_con,
    print_method,
    validate_input,
)
from SeleniumScraping.exceptions import InvalidISOError
from SeleniumScraping.filepaths import FilePaths


class ShapeFiles(object):
    """Class for handling shapefiles."""

    def __init__(self, country: str) -> None:
        self.pat_shp = re.compile(r"\.shp$")
        self.country = country
        self.iso3 = None

    @property
    def country(self) -> str:
        """Country getter."""
        return self._country

    @country.setter
    def country(self, value: str) -> None:
        """Country setter."""
        co_name = self.validate_country(value)
        assert isinstance(co_name, str)
        self._country = co_name
        # Test if shapefile already exists and if not generate it
        if not self.shp_exists():
            print_method(
                "ShapeFiles",
                f"I didn't find a shapefile for {self._country} and need to download it first.",
            )
            self.generate_shapefiles()
        else:
            print_method(
                "ShapeFiles",
                f"A shapefile for {self._country} already exists so I don't need to download it.",
            )

    def validate_country(self, country: str) -> str | None:
        """Generate ISO3 based on country.

        Parameters
        ----------
        country : str
            Country to find ISO3 for.

        Raises
        ------
        InvalidISOError
            If no ISO3 for the given country could be found.

        Returns
        -------
        iso3 : TYPE
            ISO3 of found country.
        """
        country = country.title()
        sym_dict = pd.read_feather(FilePaths.country_syms_user).to_dict(
            orient="list"
        )
        try:
            country_obj = pycountry.countries.lookup(country)
            self.iso3 = country_obj.alpha_3
            return country_obj.name
        except LookupError as invalid_excp:
            try:
                country_sym = sym_dict[country][0]
                country_obj = pycountry.countries.lookup(country_sym)
                self.iso3 = country_obj.alpha_3
                return country_obj.name
            except KeyError:
                pass
            try:
                search_co = pycountry.countries.search_fuzzy(country)

                found_co = "country" if len(search_co) == 1 else "countries"

                len_co = "one" if len(search_co) == 1 else len(search_co)

                print_method(
                    "Shapefiles",
                    f"""
                    I could not find an entry for {country}, however, I did a
                    fuzzy search and found {len_co} {found_co}.""",
                )

                for idx, co_ in enumerate(search_co):

                    _iter = idx + 1

                    _iter_msg = f"""
                    The {ordinal(_iter)} country in the list is {co_.name} with
                    the ISO {co_.alpha_3}."""

                    print_con(_iter_msg)

                    user_input = validate_input("Should I take this one?")
                    if user_input:
                        sym_dict[country] = [co_.name]
                        pd.DataFrame.from_dict(data=sym_dict).to_feather(
                            FilePaths.country_syms_user
                        )
                        sym_msg = f"""
                        I registered {country} as a valid
                        synonym for {co_.name}"""
                        print_con(sym_msg)
                        self.iso3 = co_.alpha_3
                        return co_.name

                    if len(search_co) == _iter:
                        raise InvalidISOError from invalid_excp
                    continue

            except LookupError as invalid_excp:
                raise InvalidISOError from invalid_excp

        return None

    def shp_exists(self) -> bool:
        """Test if the shapefile for the given country already exists."""
        assert isinstance(self.country, str)
        return FilePaths.shapefiles_dir_user.joinpath(
            f"{self.country.lower()}_admin.feather"
        ).exists()

    def generate_shapefiles(self) -> None:
        """Generate list with shapefiles."""
        url = f"https://biogeo.ucdavis.edu/data/diva/adm/{self.iso3}_adm.zip"

        # Create temporary directory to store the extracted shapefiles
        with TemporaryDirectory() as temp_dir:
            # Open the url zip stream from the provided url
            with urlopen(url) as zipresp:
                # Read the bytes like stream as bytes in a zipfile
                with ZipFile(BytesIO(zipresp.read())) as temp_zip:
                    # Extract the content of the file immediately without
                    # first saving the zipfile
                    temp_zip.extractall(path=temp_dir)

            # Select the most detailed shapefile by first sorting them in
            # decreasing order and then selecting the first element of the
            # resulting list
            shp_path = sorted(Path(temp_dir).rglob("*.shp"), reverse=True)[0]

            # Read the shapefile to extract the names of the municipalities
            shp_data = Reader(shp_path.as_posix())

            # Bring the shapefile data in pandas format
            pd_df = pd.DataFrame.from_dict(
                [rec_.as_dict() for rec_ in shp_data.iterRecords()]
            )

            # NOTE: it is very important to delete the "Reader" object that
            # was used to read the records of the shapefile. Otherwise the
            # tempfile cannot be deleted because the Reader object
            # continuously claims access to the shapefiles until it is
            # deleted.
            del shp_data

        # Only keep columns starting with "NAME_" as these columns contain the
        # names of the municipalities, states and so on.
        pd_df = pd_df.filter(regex=(r"^NAME_\d+"))

        # Use the following dictionary format to rename the columns appropriately.
        pd_df.rename(
            columns={
                "NAME_0": "country",
                "NAME_1": "state",
                "NAME_2": "municipality",
                "NAME_3": "county",
            },
            inplace=True,
        )

        # Create a path for the new file
        assert isinstance(self.country, str)
        feather_path = FilePaths.shapefiles_dir_user.joinpath(
            "_".join([self.country.lower(), "admin.feather"])
        )

        # Export the DataFrame as a feather file
        pd_df.to_feather(feather_path.as_posix())
