"""Scrape familysearch."""

# Future Implementations
from __future__ import annotations

# Standard Library
import logging
import os

# Standard Library
from math import ceil
from time import sleep
from typing import Literal

# Thirdparty Library
import regex as re

from func_timeout import func_set_timeout
from furl import furl
from progressbar import ETA, Counter, PercentageLabelBar, ProgressBar
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.safeguards import SafeGuards
from SeleniumScraping.driver.utils import (
    print_method,
    print_method_error,
    print_method_success,
    wait_dist,
)
from SeleniumScraping.exceptions import LastPageError

# Thirdparty Library
from func_timeout import FunctionTimedOut
from selenium.common.exceptions import TimeoutException

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.descriptors import validate_country
from SeleniumScraping.driver.history import HistoryData
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.records import RecordsData
from SeleniumScraping.driver.shapefiles import ShapeFiles
from SeleniumScraping.driver.utils import (
    print_fatal_error,
    print_iteration,
    print_method_error,
    print_section_heading,
    print_special,
)
from SeleniumScraping.exceptions import InvalidISOError, ProfileError
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.parser.processing import Processing


idx = 0
country = "Mexico"
headless = False
export_rate = 250
prof_change_rate = 500
cent_start = 1520
cent_end = 1890


driver = TorBrowser(headless=headless)
nav_fs = Navigate(driver)
hist_df = HistoryData(driver=driver, cent_start=cent_start, cent_end=cent_end)
records_df = RecordsData(driver)
data_export = Processing(driver)


country = validate_country(country).name
ShapeFiles(country)


nav_fs.navigate_to_website_login()

nav_fs.website_login()

nav_fs.navigate_to_search()

hist_df.navigate_to_records()


hist_df.set_query_parameters(country)


nav_fs.preferences_set = False

nav_fs.set_preferences_to_all_information()




# Retrieve and set the query arguments necessary for the
# familysearch query

# Set preference in "advanced search" to "all information"

# Summon the more options side page and enter the previously set
# query arguments
hist_df.start_search_query()

# If the page should contain no results then continue to the next
# page
if hist_df.no_results_found:
    hist_df.save_scrape_history()
    continue

# If the page retrieved by `set_query_parameters` is not 1 that
# means that the scraping of the specific event-place/event-time
# combination was interrupted and stopped before all pages were
# scraped. In this case we will go to the page where we last left
# off
if hist_df.page != nav_fs.get_page(peek=True):

    # Scroll down to the page end and set current page equal to
    # the page where we last left off
    nav_fs.move_to_page(hist_df.page)

else:
    # If the page retrieved by `set_query_parameters` is equal to
    # 1 then the current search query is saved to the search query
    # history
    hist_df.save_scrape_history()

# If the current page is not also the last page of the current
# query then scrape all pages until we have reached the last page
while hist_df.page != hist_df.page_max:

    # Scrape the records displayed on the current page
    records_df.scrape_elements()

    # Replace the page number of the scrape history for the
    # current municipality with the current page number to mark
    # the current page in the scrape history record as finished
    hist_df.update_scrape_history_page()

    # Scroll down to the page end and navigate to the next page
    nav_fs.next_page()

# If the current page should also be the last page of the current
# query then we only need to scrape the page and update the scrape
# history without the other two steps

# Scrape the records displayed on the current page
records_df.scrape_elements()

# Update scrape history
hist_df.update_scrape_history_page()
