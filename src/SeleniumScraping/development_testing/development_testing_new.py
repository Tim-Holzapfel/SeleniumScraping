# Future Implementations
from __future__ import annotations

# Standard Library
import atexit
import calendar
import collections
import datetime
import json
import os
import shlex
import shutil
import socket
import ssl
import subprocess
import sys
import time
import warnings
import zipfile

from configparser import ConfigParser
from dataclasses import dataclass
from datetime import datetime
from functools import partial, singledispatch
from io import BytesIO
from math import ceil
from operator import eq
from os import PathLike, get_terminal_size, getenv, startfile
from pathlib import Path
from random import sample
from secrets import choice
from subprocess import Popen
from sys import stdout
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import perf_counter, sleep
from typing import (
    Any,
    DefaultDict,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)
from urllib.request import urlopen
from zipfile import ZipFile

# Thirdparty Library
import certifi
import numpy as np
import pandas as pd
import progressbar
import psutil
import pycountry
import regex as re
import requests
import urllib3

from func_timeout import func_set_timeout
from furl import furl
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3
from geopy.location import Location
from importlib_resources import files
from numpy import dtype, float64, ndarray
from numpy.random import default_rng
from pandas.core.generic import NDFrame
from progressbar import ProgressBar
from psutil import NoSuchProcess, process_iter, wait_procs
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotSelectableException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.webdriver import (
    FirefoxProfile,
    WebDriver as Firefox,
)
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from shapefile import Reader
from termcolor import colored
from webdrivermanager import GeckoDriverManager

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.history import HistoryData
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.records import RecordsData
from SeleniumScraping.driver.shapefiles import ShapeFiles
from SeleniumScraping.driver.utils import (
    java_kill,
    load_scraped_history,
    ordinal,
    print_counter,
    print_method,
    print_method_error,
    print_method_success,
    print_special,
    start_tor,
    wait_dist,
)
from SeleniumScraping.exceptions import InvalidISOError, TorStartError
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.parser.processing import Processing, Coords
from SeleniumScraping.parser.utils import (
    ProcessDate,
    normalize_str,
    replace_whitespace,
)
from html import unescape
from SeleniumScraping.parser.processing import parser_records_export

# parser_records_export("United Kingdom")

# %% Init main classes

cent_start: int = 1520
cent_end: int = 1890
country = "Finland"

driver = TorBrowser(dev_mode=True)

nav_fs = Navigate(driver)
hist_df = HistoryData(
    driver=driver, cent_start=cent_start, cent_end=cent_end
)
records_df = RecordsData(driver)


nav_fs.load_profile()
nav_fs.user_prof


hist_df.reset_descriptors()











data_export = Processing(driver)
data_export.event_country = country

# %% Main test part


exported_data = data_export()


exported_data["female"].astype(np.single)


from sys import getsizeof


exported_data.loc[:, "female"] = exported_data["female"].astype(np.half)


exported_data["burial_date"].astype(np.int64)








getsizeof(t1)
getsizeof(t1.astype(np.half))


dir(exported_data["female"])





nav_fs.navigate_to_website_login()

nav_fs.website_login()

nav_fs.navigate_to_search()

hist_df.navigate_to_records()



hist_df.set_query_parameters(country)

nav_fs.set_preferences_to_all_information()

hist_df.start_search_query()

scraped_records = records_df.scrape_elements()


scraped_records2 = records_df.scrape_elements()


scraped_records3 = scraped_records.append(scraped_records2, ignore_index=True)


scraped_records3.drop_duplicates()

try:
    dups_count = scraped_records3.duplicated().value_counts().loc[True]
except KeyError:











export_data = Processing(driver)

records_data = RecordsData(driver)

records_data.event_country = "United Kingdom"

country = "Russia"



def valid_input():

    user_input = input("Should I take this one? [Yes/No]")

    while user_input not in ["Yes", "No"]:
        user_input = input("Please enter either Yes or No.")

    return_input = True if user_input == "Yes" else False

    return return_input



iso3 = pycountry.countries.lookup(country).alpha_3

pycountry.countries.search_fuzzy(country)



try:
    iso3 = pycountry.countries.lookup(country).alpha_3
except LookupError:
    try:
        search_co = pycountry.countries.search_fuzzy(country)

        found_co = "country" if len(search_co) == 1 else "countries"

        len_co = "one" if len(search_co) == 1 else len(search_co)

        print_method("Shapefiles", f"I could not find an entry for {country}, however, I did a fuzzy search and found {len_co} {found_co}.")

        for idx, co_ in enumerate(search_co):

            print(f"The {ordinal(idx+1)} country in the list is {co_.name} with the ISO {co_.alpha_3}.")
            user_input = valid_input()
            if user_input:
                iso3 = co_.alpha_3
                break
            else:
                continue

    except LookupError as invalid_excp:
        raise InvalidISOError from invalid_excp



import pathlib

dir(pathlib)




search_co.alpha_3



search_co = pycountry.countries.search_fuzzy("R")




import regex as re


t1 = re.compile(r"\d+")


t2 = re.escape("\d")
type(t2)




t3 = re.template("\d+")

type(t3)

t4 = re.splititer("\d+", "44")

type(t4)


from typing import Scanner


t1
type(pat_mar)

user_input = input("Enter:")


user_input in ["Yes", "No"]



import regex as re
re.ENHANCEMATCH

re.ASCII

t1 = re.compile(r"\d+", flags=re.ENHANCEMATCH|re.ASCII)


t1 = re.compile(r"\d+", flags=re.ENHANCEMATCH)

t2 = t1.flags
type(t2)
dir(t1)


regex.F
regex.V1


import regex
dir(pat_mar)

t1 = pd.NaT
type(pd.NaT)

import pandas
pandas._libs.tslibs.nattype.NaTType



regex._regex
from numpy import int64_t


re.ENHANCEMATCH|re.ASCII



pat_mar = re.compile("^M$")
pat_wid = re.compile("^W$")
to_pat = re.compile(r"(?<=\s)(to\s)")
from_pat = re.compile(r"^(from\s)")
about_after_pat = re.compile(r"^(after||about)")
pat_mis = re.compile(r"((?<![A-z])\,\s,(?=\s))|(\s\,(?=\s))|(^\,\s)")
split_pat = re.compile(r"\,\s", flags=re.REVERSE)

process_date = ProcessDate()

get_coords = Coords(driver)

records_path = Path(records_data.load_records())

re.DEFAULT_VERSION = re.V1

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
column_list = []

for l_name in ["birth", "death", "death_registration", "burial"]:
    try:
        column_list.append(columns_create(records_df, l_name))
    except KeyError:
        column_list.append(
            pd.DataFrame(
                data= [""]*len(records_df),
                index=records_df.index,
                columns=["_".join([l_name, "place"])],
            )
        )

records_places = (
    pd.concat(column_list, axis=1).filter(regex="place").fillna("")
)

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
place_record_split = (
    pd.DataFrame(
        data=[split_pat.split(str_) for str_ in records_places["place"]]
    )
    .fillna("")
    .rename(
        columns={0: "country", 1: "municipality", 2: "city", 3: "church"},
    )
    .drop(columns=["church"], errors="ignore")
)


for pat_ in [to_pat, from_pat, about_after_pat]:

    place_record_split = place_record_split.apply(
        lambda x: [pat_.sub("", str_) for str_ in x]
    )

for i in range(2):
    place_record_split = place_record_split.apply(
        lambda x: [process_date.remove_date(str_) for str_ in x]
    )

# Sort values
place_record_split.sort_values(
    by=["country", "municipality", "city"], inplace=True
)

# Apply sorted index to original DataFrame.
records_df_sorted = records_df.iloc[place_record_split.index]

records_df_sorted.reset_index(drop=True, inplace=True)


# Reset index of sorted DataFrame as well.
place_record_split_sorted = place_record_split.reset_index(drop=True)

places_unique = place_record_split_sorted.drop_duplicates()

query_series = (
    places_unique["city"]
    + ", "
    + places_unique["municipality"]
    + ", "
    + places_unique["country"]
)

query_series = pd.Series(
    [pat_mis.sub("", str_).strip() for str_ in query_series]
)

query_series = query_series.iloc[np.where(query_series != "")[0].tolist()]

query_series.drop_duplicates(inplace=True)

places_unique = places_unique.iloc[query_series.index]










geo_pd = get_coords(query_series).set_index(places_unique.index)


records_final = pd.concat([records_df_sorted, geo_pd], axis=1, join="outer")

records_final[geo_pd.columns.to_list()] = records_final[
    geo_pd.columns.to_list()
].ffill()


# %% Test Part

from tempfile import TemporaryDirectory, TemporaryFile, NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
import zipfile
from pathlib import Path

def get_strl_cols(df_: pd.DataFrame):

    strl_idx = np.where(
        ("O" == df_.dtypes).values
        * (~df_.columns.str.endswith("date"))
    )[0]

    strl_cols = df_.iloc[:, strl_idx].columns.to_list()

    return strl_cols



col_drop_list: List[str] = []
for col_ in records_df.columns.to_list():
    if (len(records_df[col_].unique())) == 1:
        col_drop_list.append(col_)


records_df.columns

t1 = records_df.apply(lambda x: not (x.unique().size == 1 and x.unique().tolist()[0] in ["", None])).pipe(np.where)[0]



def drop_empty_cols(df_: pd.DataFrame) -> pd.DataFrame:
    df_idx = df_.apply(lambda x: not (x.unique().size == 1 and x.unique().tolist()[0] in ["", None])).pipe(np.where)[0]

    return df_.iloc[:, df_idx]



drop_empty_cols(records_df)



x = records_df.iloc[:, 1]

not (x.unique().size == 1 and x.unique().tolist()[0] in ["", None])


from operator import inv


inv([True, True])







np.where(t1)
dir(t1)
t1.pipe(np.where)


t1.index

dir(t1)


t1.index
t2 = pd.Series([""])

t3 = t2.unique().tolist()[0]

t2.unique().tolist()[0] in ["", None]






dir(t2)

t3 = t2.describe()
t2.attrs

records_df = records_df.drop(columns=col_drop_list, errors="ignore")



with TemporaryDirectory(dir=FilePaths.export_dir_user_path) as temp_dir:

    export_path = FilePaths.export_dir_user_path / records_path.name.replace(".feather", ".zip")
    temp_dir = TemporaryDirectory(dir=FilePaths.export_dir_user_path)
    temp_filename = Path(temp_dir.name) / "temp_stata.dta"
    temp_arcname = temp_filename.name

    records_final.to_stata(
        temp_filename,
        data_label="Familysearch Data",
        convert_strl = get_strl_cols(records_final),
        version=117,
    )

    with ZipFile(export_path, 'w', ZIP_DEFLATED) as zip_:
        zip_.write(filename=temp_filename, arcname=temp_arcname)

    temp_dir.cleanup()


dir(temp_dir)


t5 = pd.concat(column_list).fillna("")



records_places = (
    pd.concat(column_list, axis=1).filter(regex="date").fillna("")
)


t6 = records_places["burial_date"].unique()

t6.values
dir(t6)

t6.tolist()

t7 = t2.unique().tolist()

["", None] in t7

t7 in ["", None]
t7.isna()

dir(t2.unique())


t2.unique().size

t6 != "NaT"
t2 = pd.Series([""])

