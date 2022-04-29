"""Utility functions for data export."""

# Future Implementations
from __future__ import annotations

# Standard Library
import calendar
import datetime

from pathlib import Path
from typing import Any

# Thirdparty Library
import pandas as pd
import regex as re

# Package Library
from SeleniumScraping.filepaths import FilePaths


re.DEFAULT_VERSION = re.V1


def get_prev_scraped_country() -> str:
    """Get country used previously."""
    # List containing all available records files
    record_files = list(FilePaths.records_dir.rglob("*.feather"))

    # For each records file get the time it was last modified
    records_mod_time = [fpath_.stat().st_mtime for fpath_ in record_files]

    # Combine file path with file modification time
    records_path_mod_pd = pd.DataFrame(
        {"mod_time": records_mod_time, "file_path": record_files}
    )

    # Return records file that was modified most recently
    most_recent_mod = records_path_mod_pd.loc[
        records_path_mod_pd["mod_time"].idxmax(), "file_path"
    ]

    assert isinstance(most_recent_mod, Path)

    r_country = (
        most_recent_mod.stem.replace("records_", "").replace("_", " ").title()
    )

    return r_country


def reverse_split(str_: str) -> pd.Series:
    """Reverse split order."""
    return pd.Series(str_.split(", ")[::-1])


def reverse_col_split(str_: str) -> pd.Series:
    """Reverse split order."""
    return pd.Series(str_.split(r"\n")[::-1])


def replace_whitespace(str_: str) -> list[str]:
    """Replace multiple white spaces with a single one."""
    df_return = [" ".join(str_.split()) for str_ in str_]
    return df_return


def normalize_str(df_: pd.DataFrame) -> pd.DataFrame:
    """Normalize string and remove any non-ascii characters."""
    df_normal = (
        df_.str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8", errors="ignore")
    )

    return df_normal


class ProcessDate(object):
    """Format date."""

    def __init__(self):
        # NOTE: It is necessary to have two sets of regular expressions for
        # the date: one to format the date and one for removing the date. The
        # reason is that invalid dates like "June 0024" should not be
        # recognized as dates while formatting the date but invalid dates
        # should still be removed when "remove_date" is called.
        month_name = "|".join([calendar.month_name[i] for i in range(1, 13)])
        month_abbr = "|".join([calendar.month_abbr[i] for i in range(1, 13)])

        # -------------- Regular Expression For "format_date". ------------- #

        year_pattern = r"\s[1-9]\d{3}"
        day_pattern = r"^\d{1,2}\s"

        self._dmy_pat_format = re.compile(
            day_pattern + f"({month_name})" + year_pattern
        )  # %d %B %Y
        self._dby_pat_format = re.compile(
            day_pattern + f"({month_abbr})" + year_pattern
        )  # "%d %b %Y
        self._my_pat_format = re.compile(
            f"({month_name})" + year_pattern
        )  # %B %Y
        self._by_pat_format = re.compile(
            f"({month_abbr})" + year_pattern
        )  # %B %Y
        self._y_pat_format = re.compile(r"^[1-9]\d{3}")  # %Y

        # -------------- Regular Expression For "remove_date". ------------- #

        self._dmy_pat_remove = re.compile(
            day_pattern + f"({month_name})" + r"\s\d{4}"
        )  # %d %B %Y
        self._dby_pat_remove = re.compile(
            day_pattern + f"({month_abbr})" + r"\s\d{4}"
        )  # "%d %b %Y
        self._my_pat_remove = re.compile(
            f"({month_name})" + r"\s\d{4}"
        )  # %B %Y
        self._by_pat_remove = re.compile(
            f"({month_abbr})" + r"\s\d{4}"
        )  # %B %Y
        self._y_pat_remove = re.compile(r"^\d{4}")  # %Y

    @staticmethod
    def _date_iso(date_str: str, date_format: str) -> str:
        return datetime.date.isoformat(
            datetime.datetime.strptime(date_str, date_format)
        )

    @staticmethod
    def _date_strp(date_str: str, date_format: str) -> datetime.datetime:
        return datetime.datetime.strptime(date_str, date_format)

    def extract_date(self, date_str: str) -> str | None:
        """Format date."""
        if isinstance(date_str, str):
            date_strip = date_str

            if bool(self._dmy_pat_format.search(date_str)):
                date_strip = self._dmy_pat_format.findall(date_str)[0]

            if bool(self._dby_pat_format.search(date_str)):
                date_strip = self._dby_pat_format.findall(date_str)[0]

            if bool(self._my_pat_format.search(date_str)):
                date_strip = self._my_pat_format.findall(date_str)[0]

            if bool(self._y_pat_format.search(date_str)):
                date_strip = self._y_pat_format.findall(date_str)[0]

            return date_strip.lstrip()

        return date_str

    def format_date(self, date_str: str) -> datetime.datetime | Any | None:
        """Format date."""
        if isinstance(date_str, str):  # type: ignore

            if bool(self._dmy_pat_format.search(date_str)):
                return self._date_strp(date_str, "%d %B %Y")

            if bool(self._dby_pat_format.search(date_str)):
                return self._date_strp(date_str, "%d %b %Y")

            if bool(self._my_pat_format.search(date_str)):
                return self._date_strp(date_str, "%B %Y")

            if bool(self._y_pat_format.search(date_str)):
                return self._date_strp(date_str, "%Y")

            return pd.NaT

        return date_str

    def remove_date(self, date_str: str) -> str | None:
        """Format date."""
        if isinstance(date_str, str):  # type: ignore

            date_strip = date_str

            if bool(self._dmy_pat_remove.search(date_str)):
                date_strip = self._dmy_pat_remove.sub("", date_str)

            if bool(self._dby_pat_remove.search(date_str)):
                date_strip = self._dby_pat_remove.sub("", date_str)

            if bool(self._my_pat_remove.search(date_str)):
                date_strip = self._my_pat_remove.sub("", date_str)

            if bool(self._y_pat_remove.search(date_str)):
                date_strip = self._y_pat_remove.sub("", date_str)

            return date_strip.lstrip()

        return date_str
