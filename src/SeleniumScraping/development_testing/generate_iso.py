"""Generate ISO3 based on country.."""

# Future Implementations
from __future__ import annotations

# Thirdparty Library
import pycountry
import spacy

# Package Library
from SeleniumScraping.driver.utils import (
    ordinal,
    print_con,
    print_method,
    validate_input,
)
from SeleniumScraping.exceptions import InvalidISOError


def validate_country(self, country: str) -> str | None:
    """
    Generate ISO3 based on country.

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
    try:
        country_obj = pycountry.countries.lookup(country).alpha_3
        self.iso3 = country_obj.alpha_3
        return country_obj.name
    except LookupError as invalid_excp:
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
                    self.iso3 = co_.alpha_3
                    return co_.name

                if len(search_co) == _iter:
                    raise InvalidISOError from invalid_excp
                continue

        except LookupError as invalid_excp:
            raise InvalidISOError from invalid_excp

    return None


generate_shapefiles("Russia")


dir(pycountry)

dir(pycountry.countries)

t1 = pycountry.countries

list(t1)










from SeleniumScraping.filepaths import FilePaths



FilePaths.co_syms_user.exists()


dir(FilePaths.co_syms_user)



pycountry.countries.index_names

pycountry.countries.lookup("Germany").alpha_3


import pandas as pd


dir(pd)

pd.save
import numpy as np


np.save()


