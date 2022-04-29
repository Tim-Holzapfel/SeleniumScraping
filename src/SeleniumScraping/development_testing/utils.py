"""Utility functions for data export."""
from __future__ import annotations

# Standard Library
import datetime

# Thirdparty Library
import pandas as pd
import regex as re


re.DEFAULT_VERSION = re.V1


def reverse_split(x):
    """Reverse split order."""
    return pd.Series(x.split(", ")[::-1])


def reverse_col_split(x):
    """Reverse split order."""
    return pd.Series(x.split(r"\n")[::-1])


def replace_whitespace(x):
    df_return = [" ".join(str_.split()) for str_ in x]
    return df_return


class DateFormat:
    """Format date."""

    def __init__(self):
        self._dmy_pat = re.compile(
            r"^\d{1,2}\s[A-Z][a-z]+\s\d{4}$"
        )  # %d %B %Y
        self._my_pat = re.compile(r"^[A-Z][a-z]+\s\d{4}$")  # %B %Y
        self._y_pat = re.compile(r"^\d{4}$")  # %Y

    def _date_iso(self, date_str: str, date_format: str):
        return datetime.date.isoformat(
            datetime.datetime.strptime(date_str, date_format)
        )

    def _date_strp(self, date_str: str, date_format: str):
        return datetime.datetime.strptime(date_str, date_format)

    def __call__(self, date_str: str):
        """Format date."""
        if isinstance(date_str, str):
            return (
                self._date_strp(date_str, "%d %B %Y")
                if bool(self._dmy_pat.search(date_str))
                else self._date_strp(date_str, "%B %Y")
                if bool(self._my_pat.search(date_str))
                else self._date_strp(date_str, "%Y")
                if bool(self._y_pat.search(date_str))
                else None
            )
        else:
            return date_str


def columns_create(records_data: pd.DataFrame, records_name: str):
    """Apply common scheme to the birth, death and burial columns."""
    format_date = DateFormat()

    records_copy = records_data.copy(deep=True)

    column_date = "_".join([records_name, "date"])
    column_place = "_".join([records_name, "place"])

    # Split column into event place and event date in reversed order
    split_cols = [
        re.split(
            r"(?<=\d+)\n", str_, flags=re.REVERSE, maxsplit=1, concurrent=True
        )
        for str_ in records_copy[records_name]
    ]

    # Transform split_cols, which is a list of list into a pandas DataFrame.
    records_split = pd.DataFrame(
        data=split_cols, columns=[column_place, column_date]
    )

    # Bring date in right format
    records_split[column_date] = [
        format_date(i) for i in records_split[column_date]
    ]

    # Strip whitespaces and replace multiple whitespaces with a single one
    records_split[column_place] = [
        " ".join(str_.split()) for str_ in records_split[column_place]
    ]

    return records_split
