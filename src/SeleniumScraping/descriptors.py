"""Data descriptors used throughout the project."""

# Future Implementations
from __future__ import annotations

# Standard Library
from configparser import ConfigParser
from distutils.util import strtobool
from functools import cache
from inspect import currentframe
from itertools import cycle
from os import PathLike
from pathlib import Path
from random import random, seed, shuffle
from shutil import copy2
from types import FrameType
from typing import Optional

# Thirdparty Library
import pandas as pd

from pycountry import countries
from pycountry.db import Data as Country

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.utils import (
    ordinal,
    print_con,
    print_descriptor,
    print_method,
    validate_input,
)
from SeleniumScraping.exceptions import InvalidISOError
from SeleniumScraping.filepaths import FilePaths


StrPath = str | PathLike[str]


class ProfIter(object):
    """Manage available user profiles."""

    def __init__(self):
        """Manage available user profiles."""
        path_iter = Path(FilePaths.inactive_profs_dir_user).rglob("*.ini")
        blacklist_df = pd.read_feather(FilePaths.blacklist_path)
        active_dir = FilePaths.active_profs_dir_user
        inactive_profs: list[str] = []

        for prof in path_iter:
            config = ConfigParser()
            config.read(prof)
            _phone = config["PHONE"]["phone_number"]
            _active = config["ACCOUNT"]["activated"]
            for sms_, _ in blacklist_df.itertuples(index=False):
                if sms_ == _phone:
                    prof.unlink()
            if not strtobool(_active):
                inactive_profs.append(prof.as_posix())
            else:
                copy2(prof, active_dir)
                prof.unlink()

        self.iter_prof = iter(inactive_profs)

    def __get__(
        self,
        iter_prof: object,
        objtype: Optional[type[object]] = None,
    ) -> str:
        """Retrieve list of profiles that not yet have been activated."""
        try:
            return next(self.iter_prof)
        except StopIteration as iter_error:
            print("Profile list has been exhausted!")
            raise StopIteration from iter_error


class PhoneIter(object):
    """SMS number iterator."""

    def __init__(self):
        """SMS number iterator."""
        # If the dataframe with the SMS not exists yet then generate it.
        if not FilePaths.sms_df_user.exists():
            sms_driver = TorBrowser(onion_network=False)
            sms_driver.get_sms()
            sms_driver.close_browser()

        pd_df = pd.read_feather(FilePaths.sms_df_user)

        # Remove sms number which are on the SMS blacklist
        blacklist_df = pd.read_feather(FilePaths.blacklist_path)
        pd_df = (
            pd_df.merge(right=blacklist_df, how="left", indicator=True)
            .query("_merge=='left_only'")
            .drop(columns="_merge")
        )
        pd_df.reset_index(drop=True, inplace=True)
        pd_df.to_feather(FilePaths.sms_df_user)

        # Generate random seed
        s_seed = random()

        # Set seed for the shuffling of the sms_number
        seed(s_seed)
        # shuffle(pd_df["sms_number"])

        # Set the seed again using the same seed value as for sms_number.
        # This is to make sure that even after the shuffling an English number
        # is used for England.
        seed(s_seed)
        # shuffle(pd_df["sms_country"])
        self.obj = cycle(pd_df.itertuples(index=False))

    def __get__(
        self,
        obj: object | None,
        objtype: Optional[type[object]] = None,
    ) -> tuple[str, str]:
        """Profile generator."""
        sms_number, sms_country = next(self.obj)
        return sms_number, sms_country


class UserProfiles(object):
    """Organize available profiles."""

    def __init__(self) -> None:
        """Organize available profiles."""
        path_iter = Path(FilePaths.active_profs_dir_user).rglob("*.ini")
        active_profs = ConfigParser().read(path_iter)
        shuffle(active_profs)
        self.prof_path = cycle(active_profs)

    def __get__(
        self,
        prof_path: object,
        prof_type: Optional[type[object]] = None,
    ) -> str:
        """Profile generator."""
        next_prof = next(self.prof_path)
        return next_prof


class StrDesc(object):
    """Descriptor for string variables."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for string variables.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.str_desc: str | None = None
        self.instance_name: str = instance_name

    def __get__(
        self,
        str_desc: object,
        str_type: Optional[type[object]] = None,
    ) -> str | None:
        """Get variable value."""
        return self.str_desc

    def __set__(self, str_desc: object, value: str):
        """Set variable."""
        if value is None or self.str_desc == value:
            return
        assert isinstance(value, str)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.str_desc} to {value}!",
        )
        self.str_desc = value

    def __delete__(self, str_desc: object | None) -> None:
        """Reset the descriptor."""
        self.str_desc = ""


class EventPlace(object):
    """Descriptor for event place (either country, municipality or state)."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for event places.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.

        Returns
        -------
        None
            DESCRIPTION.
        """
        self.event_place: str | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        event_place: object | None,
        event_type: Optional[type[object]] = None,
    ) -> str | None:
        """Get event type."""
        return self.event_place

    def __set__(self, event_place: object, value: str) -> None:
        """Set event type."""
        if value is None or self.event_place == value:
            return
        assert isinstance(value, str)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.event_place} to {value}!",
        )
        self.event_place = value

    def __delete__(self, event_place: object | None) -> None:
        """Reset the descriptor."""
        self.event_place = None


class EventCountry(object):
    """Descriptor for event place (either country, municipality or state)."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for event places.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.event_country: str | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        event_country: object | None,
        country_type: Optional[type[object]] = None,
    ) -> str | None:
        """Get event type."""
        return self.event_country

    def __set__(self, event_country: object, value: str) -> None:
        """Set event type."""
        if value is None or self.event_country == value:
            return
        assert isinstance(value, str)
        value = validate_country(value).name
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.event_country} to {value}!",
        )
        self.event_country = value

    def __delete__(self, event_country: object | None) -> None:
        """Reset the descriptor."""
        self.event_country = None


class CountryISO(object):
    """Descriptor for the Alpha-3 ISO of the EventCountry."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for the Alpha-3 ISO of the EventCountry.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.country_iso: str | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        country_iso: object | None,
        iso_type: Optional[type[object]] = None,
    ) -> str | None:
        """Get Country ISO."""
        return self.country_iso

    def __set__(self, country_iso: object, value: str) -> None:
        """Set Country ISO."""
        if value is None or self.country_iso == value:
            return
        assert isinstance(value, str)
        value = validate_country(value).alpha_3
        # Making sure the length of the ISO3 is exactly 3.
        assert len(value) == 3
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.country_iso} to {value}!",
        )
        self.country_iso = value

    def __delete__(self, country_iso: object | None) -> None:
        """Reset the descriptor."""
        self.country_iso = None


class UserPassword(object):
    """Descriptor for the user password."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for the user password.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.user_pw: str | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        user_pw: object | None,
        num_type: Optional[type[object]] = None,
    ) -> str | None:
        """Get variable value."""
        return self.user_pw

    def __set__(self, user_pw: object, value: str) -> None:
        """Set variable."""
        if value is None or self.user_pw == value:
            return
        assert isinstance(value, str)
        pw_sub_prev = (
            "X" * len(self.user_pw) if self.user_pw is not None else None
        )
        pw_sub = "X" * len(value)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {pw_sub_prev} to {pw_sub}!",
        )
        self.user_pw = value


class UserPath(object):
    """Descriptor for the user path."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for the user path.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.user_path: str | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        user_path: object | None,
        num_type: Optional[type[object]] = None,
    ) -> str | None:
        """Get variable value."""
        return self.user_path

    def __set__(self, user_path: object, value: str) -> None:
        """Set variable."""
        if value is None or self.user_path == value:
            return
        assert isinstance(value, str)
        path_user_prev = (
            Path(self.user_path).name if self.user_path is not None else None
        )
        path_user = Path(value).name
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {path_user_prev} to {path_user}!",
        )
        self.user_path = value


class EventYear(object):
    """Descriptor for the event year."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for the event year.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.year: int | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        year: object | None,
        year_type: Optional[type[object]] = None,
    ) -> int | None:
        """Get event type."""
        return self.year

    def __set__(self, year: object, value: int) -> None:
        """Set event type."""
        if value is None or self.year == value:
            return
        assert isinstance(value, int)
        print_descriptor(
            f"{self.instance_name}", f"changed from {self.year} to {value}!"
        )
        if value <= 0:
            raise ValueError("The year cannot be negative")
        self.year = value

    def __delete__(self, year: object | None) -> None:
        """Reset the descriptor."""
        self.year = None


class PageNumber(object):
    """Descriptor for the current page number."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for the current page number.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.page_number: int | None = None
        self.instance_name = instance_name

    def __get__(
        self,
        page_number: object | None,
        page_type: Optional[type[object]] = None,
    ) -> int | None:
        """Get page number."""
        return self.page_number

    def __set__(self, page_number: object, value: int) -> None:
        """Set page number."""
        if value is None or self.page_number == value:
            return
        assert isinstance(value, int)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.page_number} to {value}!",
        )
        if value > 49:
            raise ValueError("The page cannot exceed 49.")
        self.page_number = value

    def __delete__(self, page_number: object | None) -> None:
        """Reset the descriptor."""
        self.page_number = None


class BoolDescriptor(object):
    """Descriptor for a boolean event."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for a boolean event.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.instance_name = instance_name
        self.bool_desc: bool = False

    def __get__(
        self,
        bool_desc: object | None,
        bool_type: Optional[type[object]] = None,
    ) -> bool:
        """Get event type."""
        return self.bool_desc

    def __set__(self, bool_desc: object, value: bool) -> None:
        """Set page number."""
        if value is None or self.bool_desc == value:
            return
        assert isinstance(value, bool)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.bool_desc} to {value}!",
        )
        self.bool_desc = value

    def __delete__(self, bool_desc: object | None) -> None:
        """Reset the descriptor."""
        self.bool_desc = False


class CycleCount(object):
    """Descriptor for how many times a loop was repeated."""

    def __init__(self, instance_name: str) -> None:
        """Descriptor for how many times a loop was repeated.

        Parameters
        ----------
        instance_name : str
            Name used when referring to the instance while printing.
        """
        self.instance_name = instance_name
        self.cycle_count = 0

    def __get__(
        self,
        cycle_count: object,
        cycle_type: Optional[type[object]] = None,
    ) -> int:
        """Get event type."""
        return self.cycle_count

    def __set__(self, cycle_count: object, value: int) -> None:
        """Set page number."""
        if value is None or self.cycle_count == value:
            return
        if value == 0:
            raise ValueError
        assert isinstance(value, int)
        c_frame = currentframe()
        assert isinstance(c_frame, FrameType)
        c_frame_back = c_frame.f_back
        assert isinstance(c_frame_back, FrameType)
        print_descriptor(
            f"{self.instance_name}",
            f"was increased to {value} in {c_frame_back.f_code.co_name}!",
        )
        self.cycle_count = value

    def __delete__(self, cycle_count: object) -> None:
        """Reset the descriptor."""
        self.cycle_count = 0


@cache
def validate_country(country: str) -> Country:
    """Retrieve Country information.

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
    CountryLike
        Object containing basic country information.
    """
    country = country.title()
    sym_dict = pd.read_feather(FilePaths.country_syms_user).to_dict(
        orient="list"
    )
    try:
        country_obj = countries.lookup(country)
        return country_obj
    except LookupError as invalid_excp:
        try:
            country_obj = countries.lookup(sym_dict[country][0])
            return country_obj
        except KeyError:
            pass
        try:
            search_co = countries.search_fuzzy(country)

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
                    return co_

                if len(search_co) == _iter:
                    raise InvalidISOError from invalid_excp
                continue

        except LookupError as invalid_excp:
            raise InvalidISOError from invalid_excp

    raise InvalidISOError
