# Standard Library
import collections
import math
from configparser import ConfigParser
from functools import singledispatch
from itertools import cycle
from pathlib import Path
from random import shuffle
from time import sleep
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Literal,
    Optional,
    Sequence,
    Union,
)

# Thirdparty Library
import pandas as pd
import regex as re
from furl import furl
from progressbar import ProgressBar
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import Keys
from selenium.webdriver.support.select import Select

# Package Library
from SeleniumScraping.driver.base import DriverBase, TorBrowser
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.records import RecordsData
from SeleniumScraping.driver.utils import (
    FilePaths,
    load_scraped_data,
    load_scraped_history,
    not_none,
    sort_dataframe,
    to_snakecase,
    wait_dist,
)


_dmy_pat = re.compile(r"^\d{1,2}\s[A-Z][a-z]+\s\d{4}$")
_my_pat = re.compile(r"^[A-Z][a-z]+\s\d{4}$")
_y_pat = re.compile(r"^\d{4}$")
_date_pat = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November)?\s?\d{4}$"
)
_val_pat = re.compile(
    r"(?<=Birth|Death|Burial|Father\:|Mother\:|Spouse\:).*", flags=re.S
)
_key_pat = re.compile(r"(Birth|Death|Burial|Father|Mother|Spouse)", flags=re.S)

# %% Init main classes


query_str = "Asientos, Aguascalientes, Mexico"
year_from = 1880
year_to = 1890

driver = TorBrowser(dev_mode=False)
nav_fs = Navigate(driver)
records_df = RecordsData(driver)

nav_fs.website_login()
nav_fs.navigate_to_search()
nav_fs.navigate_to_records()


df_records: pd.DataFrame = pd.read_feather(FilePaths.records_file)

table_body = driver.find_element_by_css_selector(
    "#resultsContainer > div > div:nth-child(2) > table > tbody"
)

table_cells = table_body.find_elements_by_css_selector("tr")

return_dict = collections.defaultdict(dict)


# %% Start


i = 2
t_cell = table_cells[i]

# Name for the dictionary that is created for the current
# records entry
d_name = f"{i:03}"


t_cell.text

# -------------------------------------------------------------------------- #
#                               Dictionary Keys                              #
# -------------------------------------------------------------------------- #
key_elements = t_cell.find_elements_by_css_selector("strong")

keys_unsorted = [t_key.text for t_key in key_elements]

keys_sorted = list(sorted(keys_unsorted, key=len, reverse=True))

# -------------------------------------------------------------------------- #
#                                 Text Parts                                 #
# -------------------------------------------------------------------------- #

# Text position of first keyword
first_key_pos = re.search(f"{keys_unsorted[0]}", t_cell.text, flags=re.S).start()

# Text before first keyword appears with empty elements removed
text_first_half = list(filter(None, t_cell.text[:first_key_pos].split("\n")))

# Text after first keyword appears
text_second_half = re.search(
    f"{keys_unsorted[0]}.*", t_cell.text, flags=re.S
).group(0)

# dictionary values for the second half of the text
value_list = re.split("|".join(keys_sorted), text_second_half)[1:]

pat_misc_key = re.compile(r"^.*\:")

t_len = len(text_first_half)

# -------------------------------------------------------------------------- #
#                       Text first half dictionary loop                      #
# -------------------------------------------------------------------------- #
for idx, text_ in enumerate(text_first_half):
    value_ = text_
    if idx == 0:
        KEY_ = "respondent_name"
    elif idx == (t_len - 2):
        KEY_ = "respondent_role"
    elif idx == (t_len - 1):
        KEY_ = "collection_name"
    elif bool(pat_misc_key.search(text_)):
        KEY_ = to_snakecase(pat_misc_key.search(text_).group(0))
        value_ = pat_misc_key.sub("", text_).strip()
    else:
        continue

    return_dict[d_name][KEY_] = value_

# -------------------------------------------------------------------------- #
#                      Text second half dictionary loop                      #
# -------------------------------------------------------------------------- #
for text_, value_ in zip(keys_unsorted, value_list):
    key_ = to_snakecase(text_)
    return_dict[d_name][key_] = value_


df_records_ext = pd.DataFrame.from_dict(
    return_dict,  # type: ignore
    orient="index",
)

df_records_ext.reset_index(drop=True, inplace=True)

df_records = df_records.append(df_records_ext, ignore_index=True)

df_records.to_feather(FilePaths.records_file)
