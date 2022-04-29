from functools import cache
from typing import TYPE_CHECKING, Optional

# Thirdparty Library
import pandas as pd

from pandas.core.generic import NDFrame

# Package Library
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.utils import print_method
from SeleniumScraping.filepaths import FilePaths

from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.history import HistoryData

# %% Testing Area

driver = TorBrowser(dev_mode=True)

history_data = HistoryData(driver)

country = "Finland"
cent_start = 1550
cent_end = 1890

full_range = set(range(cent_start, cent_end + 1))


history_data.set_query_parameters(country)



scrape_hist = (
    pd.read_feather(FilePaths.history_file).query(
        f"country == '{country}'"
    )
)

for name, group in scrape_hist.groupby(["country", "state", "municipality"])["year_from"]:
    _group = set(group).intersection(full_range)
    missing_years = full_range.symmetric_difference(_group)
    break

dir(full_range)



_group = set([1540, 1550, 1551])




_group.intersection(full_range)




for name, group in scrape_hist.groupby(["country", "state", "municipality"])["year_from"]:
    _group = set(group).intersection(full_range)
    missing_years = full_range.symmetric_difference(set(_group))
    if len(missing_years) != 0:
        year_from = year_to = int(list(missing_years)[0])
        event_country, event_state, event_munic = name
        break




t1 = scrape_hist.query(
    "page != page_max"
)



t1.iloc[0][["country", "state", "municipality"]]



t2 = t1.iloc[0]


t2[["country", "state", "municipality"]]


from itertools import repeat


list(missing_years)[0]

repeat(list(missing_years)[0], 2)

t2 = list(repeat(missing_years, 2))


t5 = t6 = 1880


foo = [('x', 1), ('y', 2), ('z', 3)]
bar = bool(foo)



