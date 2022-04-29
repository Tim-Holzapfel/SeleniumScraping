"""Scrape familysearch."""

# Future Implementations
import __future__

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

from collections.abc import MutableSequence
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
import pandas.core.series
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
from pandas.core.indexes.numeric import IntegerIndex
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
from tqdm import tqdm
from webdrivermanager import GeckoDriverManager

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.history import HistoryData
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.records import RecordsData
from SeleniumScraping.driver.shapefiles import ShapeFiles
from SeleniumScraping.driver.utils import (
    java_kill,
    load_scraped_data,
    load_scraped_history,
    ordinal,
    print_counter,
    print_method,
    print_method_error,
    print_method_success,
    start_tor,
    wait_dist,
)
from SeleniumScraping.exceptions import InvalidISOError, TorStartError
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.parser.geocode import Coords, RecordsGeocode
from SeleniumScraping.parser.processing import Processing
from SeleniumScraping.parser.utils import (
    ProcessDate,
    columns_create,
    normalize_str,
    replace_whitespace,
)


# %% Init main classes














driver = TorBrowser(dev_mode=True)

export_data = Processing(driver)

export_data.event_country = "Sweden"

data_est = export_data()

if "orig_query_pd" in locals():
    print("test")
else:
    print("test2")


data_est["birth_date"] = pd.to_datetime(data_est["birth_date"])

type(z2)



t3 = pd.to_datetime(data_est["birth_date"])


import pandas as pd
query_series = pd.Series(["test1", "test2", "test3"])


from typing import MutableSequence

isinstance(query_series, MutableSequence)

reveal_type(query_series)

type(query_series)


import inspect
dir(inspect)

all([isinstance(str_, str) for str_ in query_series])



from SeleniumScraping import all_str
t1 = globals()


all_str(query_series)


all_str(query_series)


list(all_str(query_series))
for i in all_str(query_series):
    print(i)




all

dir(inspect.types)




inspect.types.GenericAlias()




t1 = data_est["death_registration_date"]
t1.unique()


convert_dates = {
    x: "td" for x in set(data_est.filter(regex=(".*_date")).columns)
}

dir(convert_dates)

convert_dates.pop("death_date")

col_drop_list = []
for col_ in list(convert_dates.keys()):
    if(len(data_est[col_].unique())) == 1:
        col_drop_list.append(col_)


data_est_final = data_est.drop(columns=col_drop_list, errors="ignore")



[data_est[col_].dtype for col_ in data_est.columns.to_list()]

data_est.dtypes

event_country = "Finland"

query_path = (
    FilePaths.query_dir
    / f"{event_country.lower()}_records_query.feather"
)

# Test whether geocoding history exists.
if query_path.exists():
    print(f"I found a geocoding history for {self.event_country}!")
    orig_query_pd = pd.read_feather(query_path)


data_est.dtypes.isin(["o"])


t1 = data_est.dtypes
set(t1).issubset(["O"])



eq(data_est.dtypes, ["O"])

t2 = (t1 == ["O"]*40).values
t3 = ~data_est.columns.str.endswith("date")

strl_idx = np.where(t2 * t3)[0].tolist()


strl_idx = np.where(("O" == data_est.dtypes).values * (~data_est.columns.str.endswith("date")))[0]



data_est.filter(regex="[^date]")


data_est.columns.to_list()[strl_idx]


data_est.iloc[:,strl_idx]



dir(strl_idx)

strl_idx.index

t2 and t3
t2.all()



False * True




dir(t2)

t2.values

dir(t1)

t1.dtypes



t1.str.endswith("date")


dir(t1.str)



pd.NaT

data_est.loc[3, "death_date"]


dir(data_est)


data_est["death_date"]


t1 = data_est[["death_date"]]
convert_dates = {"death_date": "td"}
file_path = "C:/Users/Tim/Desktop/stata_test.dta"
t1.to_stata(file_path, convert_dates=convert_dates)

data_est["death_date"].str.replace("", pd.NaT)

data_est["death_date"].asfreq("D")

datetime.datetime()
datetime.datetime.strptime(, date_format)


dir(datetime.datetime)

datetime.datetime.isoformat()



data_est["burial_date"].unique()
data_est["birth_date"]




records_geocode = RecordsGeocode(driver)

records_geocode.event_country = "Sweden"

records_path = records_geocode.load_records()
get_coords = Coords(driver)


query_series = records_geocode()

geo_pd = get_coords(query_series)



sweden_geocodes = records_geocode()


rename_dict = dict({0: "address", 1: "lat", 2: "lng", 3: "alt"})

new_query_pd = pd.DataFrame(
    data=[get_coords.get_features(str_) for str_ in geo_pd["location"]]
).rename(columns=rename_dict)

new_query_pd["query"] = geo_pd["query"]
new_query_pd = new_query_pd[["query"] + list(rename_dict.values())].reset_index(drop=True)






new_query_pd.rename(columns=rename_dict)






t1 = ["query"] + list(rename_dict.values())

dir(rename_dict)



dir(rename_dict.values())







nav_fs = Navigate(driver)

hist_df = HistoryData(driver, cent_start=1550, cent_end=1890)

records_df = RecordsData(driver)

process_date = ProcessDate()

export_data = Processing(driver)

get_coords = Coords(driver)

# %% Start Function

# Func Args
country = "Mexico"

# Func Body

re.DEFAULT_VERSION = re.V1

to_pat = re.compile(r"(?<=\s)(to\s)")
from_pat = re.compile(r"^(from\s)")
about_after_pat = re.compile(r"^(after||about)")
pat_mis = re.compile(r"((?<![A-z])\,\s,(?=\s))|(\s\,(?=\s))|(^\,\s)")
split_pat = re.compile(r"\,\s", flags=re.REVERSE)

export_data.event_country = country

records_path = export_data.load_records()


records_df: pd.DataFrame = (
    pd.read_feather(records_path)
    .reset_index(drop=True)
    .fillna("")
    .apply(replace_whitespace)
    .apply(normalize_str)
)

column_list = []

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

del burial_columns, death_columns, death_registration_columns, birth_columns

records_places["place"] = records_places.apply(
    lambda row: row["death_registration_place"]
    if row["death_registration_place"] != ""
    else row["burial_place"]
    if row["burial_place"] != ""
    else row["death_place"],
    axis=1,
)

place_record_split = pd.DataFrame(
    data=[split_pat.split(str_) for str_ in records_places["place"]]
).fillna("")

place_record_split.rename(columns={0: "country", 1:"municipality", 2:"city", 3:"church"}, inplace=True)

place_record_split.drop(columns=["church"], inplace=True, errors="ignore")

place_record_split["country"] = [to_pat.sub("", str_) for str_ in place_record_split["country"]]
place_record_split["municipality"] = [to_pat.sub("", str_) for str_ in place_record_split["municipality"]]
place_record_split["city"] = [to_pat.sub("", str_) for str_ in place_record_split["city"]]

place_record_split["country"] = [from_pat.sub("", str_) for str_ in place_record_split["country"]]
place_record_split["municipality"] = [from_pat.sub("", str_) for str_ in place_record_split["municipality"]]
place_record_split["city"] = [from_pat.sub("", str_) for str_ in place_record_split["city"]]

place_record_split["country"] = [about_after_pat.sub("", str_) for str_ in place_record_split["country"]]
place_record_split["municipality"] = [about_after_pat.sub("", str_) for str_ in place_record_split["municipality"]]
place_record_split["city"] = [about_after_pat.sub("", str_) for str_ in place_record_split["city"]]



place_record_split["country"] = [process_date.remove_date(str_) for str_ in place_record_split["country"]]
place_record_split["municipality"] = [process_date.remove_date(str_) for str_ in place_record_split["municipality"]]
place_record_split["city"] = [process_date.remove_date(str_) for str_ in place_record_split["city"]]

place_record_split["country"] = [process_date.remove_date(str_) for str_ in place_record_split["country"]]
place_record_split["municipality"] = [process_date.remove_date(str_) for str_ in place_record_split["municipality"]]
place_record_split["city"] = [process_date.remove_date(str_) for str_ in place_record_split["city"]]

# Sort values
place_record_split.sort_values(by=["country", "municipality", "city"], inplace=True)

# Apply sorted index to original DataFrame.
records_df = records_df.iloc[place_record_split.index]


records_df.reset_index(drop=True, inplace=True)

# Reset index of sorted DataFrame as well.
place_record_split.reset_index(drop=True, inplace=True)



places_unique = place_record_split.drop_duplicates()

query_series = places_unique["city"] + ", " + places_unique["municipality"] + ", " + places_unique["country"]


query_series = pd.Series([pat_mis.sub("", str_).strip() for str_ in query_series])

geo_pd = get_coords(query_series)

geo_pd.set_index(places_unique.index, inplace=True)

records_final = pd.concat([records_df, geo_pd], axis=1, join="outer")


records_final[geo_pd.columns.to_list()] = records_final[geo_pd.columns.to_list()].ffill()











records_final_sub = records_final.iloc[0:1000]

records_df_sub = records_df.iloc[1:1000]



pycountry.countries.lookup("United Kingdom")




geo_pd_test = geo_pd.copy()




geo_pd_test.set_index(places_unique.index, inplace=True)


query_series_sub.isin(geo_pd_test["query"])



t1 = geo_pd_test["query"].isin(query_series_sub)
t2 = np.where(t1)[0]


rand_index = geo_pd_test["query"].index.to_series().sample(20).index.sort_values()


sample_query = geo_pd_test.loc[rand_index, "query"]

sample_query = sample_query.append(pd.Series(["Test Query String"]))
dir(sample_query)



geo_index = np.where(geo_pd_test["query"].isin(sample_query))









query_path = FilePaths.query_dir / f"{get_coords.event_country.lower()}_records_query.feather"

query_pd = pd.read_feather(query_path)

index_test = np.where(~sample_query.isin(geo_pd_test["query"]))[0]

extra_query = sample_query.iloc[index_test]



geo_pd.to_feather(query_path)



get_coords.event_country.lower()






type(query_series)




dir(pandas.core.series)


pandas.core.indexes.numeric.Int64Index





isinstance(places_unique.index, IntegerIndex)



#%% Func body

query_series = pd.Series([pat_mis.sub("", str_).strip() for str_ in query_series]).iloc[0:10]

query_series = query_series.append(pd.Series(["Test Query String"])).reset_index(drop=True)


assert isinstance(query_series, pd.Series)

assert all([isinstance(str_, str) for str_ in query_series])

query_path = FilePaths.query_dir / f"{get_coords.event_country.lower()}_records_query.feather"

orig_query_pd = pd.read_feather(query_path)

# Locations that have not already been geocoded, thus strings not part of the query DataFrame.
query_miss_index = np.where(~query_series.isin(orig_query_pd["query"]))[0]

if len(query_miss_index) >= 1:

    geo_pd = pd.DataFrame(query_series.iloc[query_miss_index], columns=["query"])

    geo_pd["location"] = geo_pd["query"].progress_apply(self.geocode)

    columns = ["address", "lat", "lng", "alt"]

    new_query_pd = pd.DataFrame(
        data=[self.get_features(str_) for str_ in geo_pd["location"]],
        columns=columns,
    )

    new_query_pd["query"] = geo_pd["query"]
    new_query_pd = geo_pd[["query"] + columns].reset_index(drop=True)

    orig_query_pd = orig_query_pd.append(new_query_pd)
    orig_query_pd.to_feather(query_path)

query_pd = pd.DataFrame(query_series, columns=["query"]).set_index(keys=["query"], drop=True)

orig_query_pd.set_index(keys=["query"], drop=True, inplace=True)

return_pd = query_pd.join(orig_query_pd, how="inner").reset_index()



np.ndarray


query_pd.join(orig_query_pd, on=["query"])






query_index = np.where(orig_query_pd["query"].isin(query_series))[0]

return orig_query_pd.iloc[query_index]



np.array_like

type(query_index)



type(query_index[0])





































places_unique.index
type(places_unique.index)


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

geolocator = GoogleV3(
    api_key=FilePaths.google_key, timeout=20, ssl_context=ctx
)
geocode = RateLimiter(
    geolocator.geocode, min_delay_seconds=2, max_retries=5
)



query_pd = pd.DataFrame(query_series_sub, columns=["query"])








query_pd['location'] = query_pd['query'].progress_apply(geocode)



def get_features(geo: Location) -> List[Union[str, float, None]]:
    """Get features from geodata."""
    if geo is None:
        return [np.nan, np.nan, np.nan, np.nan]

    return [geo.address, geo.latitude, geo.longitude, geo.altitude]



geo_pd = pd.DataFrame(data = [get_features(str_) for str_ in query_pd["location"]],
                      columns=["address", "lat", "lng", "alt"])






t1 = query_series_sub.to_list()


[isinstance(str_, str) for str_ in query_series_sub]



query_pd

dir(t1)





class Coords:
    """Retrieve coordinates from googlemaps."""

    tqdm.pandas()

    def __init__(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        geolocator = GoogleV3(
            api_key=FilePaths.google_key, timeout=20, ssl_context=ctx
        )
        self.geocode = RateLimiter(
            geolocator.geocode, min_delay_seconds=2, max_retries=5
        )

    def get_features(self, geo: Location) -> List[Union[str, float, None]]:
        """Get features from geodata."""
        if geo is None:
            return [np.nan, np.nan, np.nan, np.nan]

        return [geo.address, geo.latitude, geo.longitude, geo.altitude]

    def __call__(self, query_series: pd.Series) -> List[Union[str, float, None]]:

        query_pd = pd.DataFrame(query_series, columns=["query"])

        query_pd['location'] = query_pd['query'].progress_apply(self.geocode)

        columns=["address", "lat", "lng", "alt"]

        geo_pd = pd.DataFrame(data = [self.get_features(str_) for str_ in query_pd["location"]],
                              columns=columns)

        geo_pd["query"] = query_pd['query']

        return geo_pd[["query"] + columns]










place_country = place_record_split[["country"]]


place_mexico = place_country[place_country == "Mexico"]



mexico_index = pd.Series(np.where(place_country == "Mexico")[0].tolist())
sweden_index = pd.Series(np.where(place_country == "Sweden")[0].tolist())
finland_index = pd.Series(np.where(place_country == "Finland")[0].tolist())


records_mexico = records_orig.loc[mexico_index, :]
records_mexico.reset_index(drop=True, inplace=True)
records_mexico_path = FilePaths.records_dir / "records_mexico.feather"
records_mexico.to_feather(records_mexico_path)




records_sweden = records_orig.loc[sweden_index, :]
records_sweden.reset_index(drop=True, inplace=True)
records_sweden_path = FilePaths.records_dir / "records_sweden.feather"
records_sweden.to_feather(records_sweden_path)





records_finland = records_orig.loc[finland_index, :]
records_finland.reset_index(drop=True, inplace=True)
records_finland_path = FilePaths.records_dir / "records_finland.feather"
records_finland.to_feather(records_finland_path)



dir(mexico_index)
mexico_index.tolist()


place_country = place_record_split.drop(columns=["city"]).groupby(["country"]).agg({"count"})




dir(place_country)
















records_str = "from 27 January 1889 to 2 February 1889 Phila."




place_record_unqiue = place_record_split.drop_duplicates()














query_str_sub = query_str.iloc[1:10]



get_coords = Coords()





















query_str = place_record_split[["query_str"]].drop_duplicates().dropna().reset_index(drop=True)



str_ = query_str.iloc[0].item()
