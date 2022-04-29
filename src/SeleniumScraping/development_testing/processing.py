"""Prepare data for export."""
from __future__ import annotations

# Standard Library
from typing import List

# Thirdparty Library
import numpy as np
import pandas as pd
import regex as re
from pandas.core.generic import NDFrame

# Package Library
from SeleniumScraping.driver.utils import print_method
from SeleniumScraping.parser.utils import columns_create, replace_whitespace, DateFormat
from SeleniumScraping.filepaths import FilePaths


records_df = pd.read_feather(FilePaths.records_file)

# Replacing missing values with an empty string
records_df.fillna("", inplace=True)

format_date = DateFormat()


# %% Start function

records_copy = records_df.copy(deep=True)

records_name = "death"

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

# Split column into event place and event date in reversed order
death_place_split = [
    re.split(
        r"\,\s", str_, flags=re.REVERSE
    )
    for str_ in records_split["death_place"]
]

death_place_split_df = pd.DataFrame(
    data=death_place_split
)

death_place_split_df.fillna("", inplace=True)

# Strip whitespaces and replace multiple whitespaces with a single one
death_place_split_df = [
    " ".join(str_.split()) for str_ in death_place_split_df
]


# Name of columns of type string
str_columns = [
    str_
    for str_ in death_place_split_df.columns.to_list()
    if not str_.endswith("date")
]

# Strip whitespaces and replace multiple whitespaces with a single one
death_place_split_df[str_columns] = death_place_split_df.loc[:, str_columns].apply(
    replace_whitespace
)




































def export_data() -> None:
    """Export collected data."""
    export_path = FilePaths.export_dir_user_path / "records_data.dta"

    if export_path.exists():
        export_path.unlink()

    pat_mar = re.compile("^M$")
    pat_wid = re.compile("^W$")

    re.DEFAULT_VERSION = re.V1

    # Making sure the folder in which the file is going to be exported to
    # exists
    assert export_path.parent.exists()

    # Making sure the export path has the right file ending
    assert export_path.suffix == ".dta"

    records_df = pd.read_feather(FilePaths.records_file)

    # Replacing missing values with an empty string
    records_df.fillna("", inplace=True)

    # ---------------------------------------------------------------------- #
    #                  Seperate event_date from event_place                  #
    # ---------------------------------------------------------------------- #

    column_list: List[NDFrame] = []

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

    records_df.drop(
        columns=[
            "birth",
            "death",
            "burial",
            "death_registration",
        ],
        inplace=True,
        errors="ignore",
    )

    # Append main dataframe to the list of columns
    column_list.append(records_df)

    # Concatenate newly created columns
    records_df = pd.concat(column_list, axis=1)

    # Name of columns of type string
    str_columns = [
        str_
        for str_ in records_df.columns.to_list()
        if not str_.endswith("date")
    ]

    # Strip whitespaces and replace multiple whitespaces with a single one
    records_df[str_columns] = records_df.loc[:, str_columns].apply(
        replace_whitespace
    )

    # ---------------------------------------------------------------------- #
    #                          Adjust marital values                         #
    # ---------------------------------------------------------------------- #

    if "marital_status" in set(records_df.columns):

        # Replace "marital_status" with "Married" if "marital_status" is "M"
        records_df["marital_status"] = [
            pat_mar.sub(str_, "Married")
            if bool(pat_mar.search(str_))
            else str_
            for str_ in records_df["marital_status"]
        ]

        # Replace "marital_status" with "Widowed" if "marital_status" is "W"
        records_df["marital_status"] = [
            pat_wid.sub(str_, "Widowed")
            if bool(pat_wid.search(str_))
            else str_
            for str_ in records_df["marital_status"]
        ]

        # Normalizing string columns and removing all non ASII character
        records_df[str_columns] = records_df[str_columns].apply(
            lambda x: x.str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )

    # Create dictionary of available dates with the date format set to "td"
    convert_dates = {
        x: "td" for x in set(records_df.filter(regex=(".*_date")).columns)
    }

    # ---------------------------------------------------------------------- #
    #                          Adjust gender values                          #
    # ---------------------------------------------------------------------- #

    if "sex" in set(records_df.columns):

        pat_m = re.compile("Male")
        pat_f = re.compile("Female")
        put_u = re.compile("Unknown")

        records_df["sex"] = [
            0
            if bool(pat_m.search(str_))
            else 1
            if bool(pat_f.search(str_))
            else np.nan
            if bool(put_u.search(str_))
            else str_
            for str_ in records_df["sex"]
        ]

        records_df.rename(columns={"sex": "female"}, inplace=True)

    # -------------------------------------------------------------------------- #
    #                            Adjusting age values                            #
    # -------------------------------------------------------------------------- #

    if "age" in set(records_df.columns):

        pat_num = re.compile(r"\d+")
        pat_month = re.compile(r"\d+m")
        pat_day = re.compile(r"\dd")

        records_df["age2"] = [
            round(int(pat_num.findall(str_)[0]) / 365, 3)
            if bool(pat_day.search(str_))
            else round(int(pat_num.findall(str_)[0]) / 12, 3)
            if bool(pat_month.search(str_))
            else np.nan
            if str_ == ""
            else float(str_)
            for str_ in records_df["age"]
        ]

        records_df["age2"].astype(float)

    records_df.rename(columns={"ethnicity": "nationality"}, inplace=True)

    # Reorder columns
    records_df = records_df[sorted(records_df.columns.to_list())]

    # Export data in Stata format
    records_df.to_stata(
        export_path,
        convert_dates=convert_dates,
        write_index=False,
        data_label="Familysearch Data",
    )

    print_method("export_data", "I succesfully exported the data!")
