"""Data descriptors used throughout the project."""

# Future Implementations
from __future__ import annotations

# Standard Library
from configparser import ConfigParser
from distutils.util import strtobool
from itertools import cycle
from pathlib import Path
from random import random, seed, shuffle
from shutil import copy2
from typing import List, Optional, Tuple, Union

# Thirdparty Library
import pandas as pd

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.generate.utils import print_descriptor


class ProfIter:
    """Manage available user profiles."""

    def __init__(self):
        path_iter = Path(FilePaths.inactive_profs_dir_user).rglob("*.ini")
        blacklist_df = pd.read_feather(FilePaths.blacklist_path)
        active_dir = FilePaths.active_profs_dir_user
        inactive_profs: List[str] = []

        for prof in path_iter:
            config = ConfigParser()
            config.read(prof)
            _phone = config["PHONE"]["phone_number"]
            _active = config["ACCOUNT"]["activated"]
            for sms_, _ in blacklist_df.itertuples(index=False):
                if sms_ == _phone:
                    prof.unlink()
                    continue
            if not strtobool(_active):
                inactive_profs.append(prof.as_posix())
            else:
                copy2(prof, active_dir)
                prof.unlink()

        self.iter_prof = iter(inactive_profs)

    def __get__(
        self,
        inactive_profs: Union[object, None],
        objtype: Optional[type[object]] = None,
    ) -> str:
        """Retrieve list of profiles that not yet have been activated."""
        try:
            return next(self.iter_prof)
        except StopIteration as iter_error:
            print("Profile list has been exhausted!")
            raise StopIteration from iter_error


class PhoneIter:
    """SMS number iterator."""

    def __init__(self):
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
        shuffle(pd_df["sms_number"])

        # Set the seed again using the same seed value as for sms_number.
        # This is to make sure that even after the shuffling an English number
        # is used for England.
        seed(s_seed)
        shuffle(pd_df["sms_country"])
        self.obj = cycle(pd_df.itertuples(index=False))

    def __get__(
        self,
        obj: Union[object, None],
        objtype: Optional[type[object]] = None,
    ) -> Tuple[str, str]:
        """Profile generator."""
        sms_number, sms_country = next(self.obj)
        return sms_number, sms_country


class StrDesc:
    """Descriptor for string variables."""

    def __init__(self, instance_name: str) -> None:
        self.str_desc: Union[str, None] = None
        self.instance_name: str = instance_name

    def __get__(
        self,
        str_desc: Union[object, None],
        str_type: Union[type[object], None] = None,
    ) -> Union[str, None]:
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

    def __delete__(self, str_desc: Union[object, None]) -> None:
        self.str_desc = None


class NumDesc:
    """Descriptor for numeric variables."""

    def __init__(self, instance_name: str) -> None:
        self.num_desc: Union[int, None] = None
        self.instance_name = instance_name

    def __get__(
        self,
        num_desc: Union[object, None],
        num_type: Optional[type[object]] = None,
    ) -> Union[int, None]:
        """Get variable value."""
        return self.num_desc

    def __set__(self, num_desc: object, value: str):
        """Set variable."""
        if value is None or self.num_desc == value:
            return
        assert isinstance(value, int)
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.num_desc} to {value}!",
        )
        self.num_desc = value


class UserPassword:
    """Descriptor for numeric variables."""

    def __init__(self, instance_name: str) -> None:
        self.user_pw: Union[str, None] = None
        self.instance_name = instance_name

    def __get__(
        self,
        user_pw: Union[object, None],
        num_type: Union[type[object], None] = None,
    ) -> Union[str, None]:
        """Get variable value."""
        return self.user_pw

    def __set__(self, user_pw: object, value: str) -> None:
        """Set variable."""
        if value is None or self.user_pw == value:
            return
        assert isinstance(value, str)
        pw_sub = "X" * len(value)  # type: ignore
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.user_pw} to {pw_sub}!",
        )
        self.user_pw = value


class UserPath:
    """Descriptor for numeric variables."""

    def __init__(self, instance_name: str) -> None:
        self.user_path: Union[str, None] = None
        self.instance_name = instance_name

    def __get__(
        self,
        user_path: Union[object, None],
        num_type: Union[type[object], None] = None,
    ) -> Union[str, None]:
        """Get variable value."""
        return self.user_path

    def __set__(self, user_path: object, value: str) -> None:
        """Set variable."""
        if value is None or self.user_path == value:
            return
        assert isinstance(value, str)
        path_user = Path(value).name  # type: ignore
        print_descriptor(
            f"{self.instance_name}",
            f"changed from {self.user_path} to {path_user}!",
        )
        self.user_path = value
