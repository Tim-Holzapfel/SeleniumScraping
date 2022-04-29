"""Base class for all classes depending on Selenium."""

# Future Implementations
from __future__ import annotations

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


# -------------------------------------------------------------------------- #
#                              Driver Safeguards                             #
# -------------------------------------------------------------------------- #


class DriverBase(SafeGuards):
    """Base class for all classes depending on Selenium."""

    def __init__(
        self,
        driver: TorBrowser,
    ) -> None:
        """Initiate base class.

        Parameters
        ----------
        driver : TorBrowser
            Modified Firefox browser routed through the onion network.
        """
        self.driver = driver
        self.scroll_top = "return arguments[0].scrollTop;"
        self.pat_num = re.compile(r"\d+")

        super().__init__(driver)

    @func_set_timeout(timeout=80)
    def get_page(self, peek: bool = False, verbose: bool = True) -> int:
        """Get current page as integer.

        Parameters
        ----------
        peek : bool, optional
            Return current page without modifying the descriptors `page` or
            `page_max`. The default is False.
        verbose : bool, optional
            Print information about the old and new page values to the
            standard console. The default is True.

        Returns
        -------
        int
            The current page number.
        """
        # Current property value of the page element at the bottom of the page
        # which equals the current page number as reported by dynamic input
        # element
        page_input_page = int(
            self.driver.find_by_css("div[pageno] input").get_property("value")
        )

        # Page label reporting the current page and the total number of pages
        # at the bottom of the page
        page_label = self.driver.find_by_css(
            "button[aria-label^='Go to next Page']"
        ).get_attribute("aria-label")

        # Regular expression extracting all numbers from the page label at the
        # bottom of the page
        page_label_regex = re.findall("\\d+", page_label)

        # The page label MUST contain exactly two numbers: the current page
        # and the total number of pages. Otherwise something IS wrong.
        assert (
            len(page_label_regex) == 2
        ), "The page label did not report exactly two numbers."

        # Current page taken from the page label at the bottom of the page
        page_label_page = int(page_label_regex[0])

        # Maximum number of pages for the given query taken from the page
        # label at the bottom of the page
        page_label_max_page = int(page_label_regex[1])

        # Test to make sure that the current page is equal to the url page
        try:
            # Current page as taken from the current url of the website.

            # NOTE: familysearch.org starts the page count in the url at zero
            # at not at one. To account for that the `url_page` has to be
            # increased by one.
            page_url_page = (
                int(furl(self.driver.current_url).query.params["offset"])
                // 100
                + 1
            )
            # If the current page is also the first page the url is not going
            # to contain an "offset" parameter which is, however, crucial for
            # determining the current page using the url. Hence, if an
            # "KeyError" is raised due to the absence of an "offset"
            # parameter then it is reasonable to assume that the current page
            # is the first page (page "1").
        except KeyError:
            page_url_page = 1

        # Because we always set the number of results per page to onehundred,
        # that means that the total number of pages for the current search
        # MUST equal the number of total results for the current query
        # divided by onehundred.  If the division contains an remainder than
        # the total number of pages is going to be equal to the ceiling of
        # the division with the last page containing the division's
        # remainder.

        # NOTE: Because familysearch.org introduced a page limit of 49 pages
        # per query, the total number of pages needs to be capped at 49,
        # which is why the min() function is included.
        page_logic_max_page = min([49, ceil(self.get_filter_results() / 100)])

        assert (
            page_logic_max_page == page_label_max_page
        ), """The maximum number of pages as reported by the page label is
        not the same as the logical total number of pages."""

        assert (
            page_input_page == page_url_page
        ), "The current page as reported by the page label is not the same as url page."

        if not peek:
            self.page = page_label_page
            self.page_max = page_label_max_page
            if verbose:
                print_method(
                    "get_current_page_number",
                    f"Setting current page to {page_label_page} and page_max to {page_label_max_page}.",
                )

        return page_label_page

    @func_set_timeout(timeout=80)
    def get_filter_results(self) -> int:
        """Get number of found records."""
        while True:
            # Test for no results found
            try:
                self.driver.find_by_css("div[data-testid='noResults'] h4")
                self.no_results_found = True
                print_method_error(
                    "get_filter_results",
                    "No results found! Continuing to next page.",
                )
                return 999
            except NoSuchElementException:
                self.no_results_found = False
            try:
                self.botcheck_test()
                filter_results = self.driver.find_by_css(
                    "#resultsContainer h5"
                ).text

                return int("".join(self.pat_num.findall(filter_results)))
            except NoSuchElementException:
                sleep(1)
            except ValueError:
                sleep(1)
            except StaleElementReferenceException:
                self.driver.refresh()
                sleep(1)

    @func_set_timeout(timeout=80)
    def check_page_loaded(self) -> None:
        """Wait for the page to be loaded."""
        # Time the function was called.
        print_method(
            "check_page_loaded",
            "I'm waiting for the page to load...",
        )
        while True:
            # Make sure page has properly loaded by trying to get the number
            # of found records.
            results = self.get_filter_results()
            if results > 0:
                print("")
                print_method_success("check_page_loaded", "page loaded!")
                break
            sleep(1)

    @func_set_timeout(timeout=80)
    def get_current_url(self) -> str:
        """Get URL of the current page."""
        current_url = furl(self.driver.current_url).pathstr
        return current_url

    @func_set_timeout(timeout=80)
    def wait_for_url_change(self, current_url: str) -> None:
        """Wait until the website has changed.

        Parameters
        ----------
        current_url : str
            Url of the current page.

        Raises
        ------
        TimeoutError
            If the website changes takes louder than 15 seconds.

        Returns
        -------
        None.
        """
        while True:
            print_method(
                "wait_for_url_change",
                "I'm waiting for the URL to change...",
            )
            new_url = furl(self.driver.current_url).pathstr
            if new_url != current_url:
                print("")
                print_method_success("wait_for_url_change", "url changed!")
                break

    def set_page_size(self) -> None:
        """Set number of records to show per page."""
        # Element containing the page selection tab
        page_dropdown = self.driver.wait_for_element_clickable(
            "#paginator-per-page"
        )

        # Get currently active page size
        page_value_ = page_dropdown.get_property("value")

        if page_value_ == "100":
            return

        # Using convenience wrapper "Select"
        Select(page_dropdown).select_by_visible_text("100")
        print_method_success("set_page_size", "page size set to 100!")
        # Making sure page has properly loaded
        self.check_page_loaded()

    @func_set_timeout(timeout=200)
    def scroll_main_page(
        self, scroll_direction: Literal["up", "down"] = "down"
    ) -> None:
        """Scroll main element of page up or down.

        Parameters
        ----------
        scroll_direction : {"up", "down"}, optional
            Direction in which to scroll. The default is "down".

        Returns
        -------
        None.
        """
        key_dir = (
            Keys.PAGE_DOWN if scroll_direction == "down" else Keys.PAGE_UP
        )

        self.driver.set_window_size(3000, 3000)

        # Results table element
        page_root = self.driver.find_by_css(":root")

        # Max possible scroll
        scroll_max = self.driver.execute_script(
            "return arguments[0].scrollTopMax;", page_root
        )

        # Focus main page
        self.driver.execute_script("arguments[0].focus();", page_root)

        # Decide which value should be targeted: if the scroll direction is
        # up then the target value should be 0 as 0 means the top of the
        # scroll bar otherwise it should be scroll_max.
        scroll_opt = scroll_max if scroll_direction == "down" else 0

        current_scroll = self.driver.execute_script(
            self.scroll_top, page_root
        )

        while current_scroll != scroll_opt:
            # Send either a page up or down keystroke
            ActionChains(self.driver).send_keys(key_dir).perform()

            # Retrieve current position on page
            current_scroll = self.driver.execute_script(
                self.scroll_top, page_root
            )

            sleep(wait_dist(1, 0.8).item())

    @func_set_timeout(timeout=200)
    def scroll_inner_page(
        self, scroll_direction: Literal["up", "down"] = "down"
    ) -> None:
        """Scroll inner page either up or down.

        Parameters
        ----------
        scroll_direction : {"up", "down"}, optional
            Direction in which to scroll. The default is "down".

        Returns
        -------
        None.
        """
        key_dir = (
            Keys.PAGE_DOWN if scroll_direction == "down" else Keys.PAGE_UP
        )

        self.driver.set_window_size(3000, 3000)

        # Results table element
        results_con = self.driver.find_by_css("#resultsContainer")

        # Max possible scroll
        scroll_max = self.driver.execute_script(
            "return arguments[0].scrollTopMax;", results_con
        )

        # Focus results table
        self.driver.execute_script("arguments[0].focus();", results_con)

        # Decide which value should be targeted: if the scroll direction is
        # up then the target value should be 0 as 0 means the top of the
        # scroll bar otherwise it should be scroll_max.
        scroll_opt = scroll_max if scroll_direction == "down" else 0

        # Retrieve current position on page
        current_scroll = self.driver.execute_script(
            self.scroll_top, results_con
        )

        bar_text = colored("Scrolling: ", "blue", attrs=["bold"])

        widgets = [
            bar_text,
            Counter(),
            " of ",
            str(scroll_max),
            " ",
            PercentageLabelBar(),
            " (",
            ETA(),
            ") ",
        ]

        scroll_prog = ProgressBar(
            max_value=scroll_max,
            initial_value=current_scroll,
            widgets=widgets,
        )

        with scroll_prog as p_bar:
            while current_scroll != scroll_opt:
                # Send a "page down" keystroke
                ActionChains(self.driver).send_keys(key_dir).perform()

                # Retrieve current position on page
                current_scroll = self.driver.execute_script(
                    self.scroll_top, results_con
                )

                sleep(wait_dist(1, 0.8).item())
                p_bar.update(current_scroll)

    @func_set_timeout(timeout=80)
    def next_page(self) -> None:
        """Navigate to next page."""
        self.scroll_inner_page()

        next_page_button = self.driver.find_by_css(
            'button[aria-label*="Go to next Page"]'
        )

        if not next_page_button.is_enabled():
            raise LastPageError("next_page: Last page reached!")

        # Click on the next page button
        next_page_button.click()

        sleep(1)

        # Make sure page has properly loaded
        self.check_page_loaded()

        # Setting the page variable according to the information supplied by
        # by the url of the current page
        self.get_page()

    @func_set_timeout(timeout=80)
    def move_to_page(self, page_num: int) -> None:
        """Move to specified page number.

        Parameters
        ----------
        page_num : int
            Number of the page that should be moved to.

        Returns
        -------
        None.
        """
        self.scroll_inner_page()

        page_selection = self.driver.find_by_css(
            "input[aria-describedby='page-number']"
        )

        actions_ = ActionChains(self.driver)

        actions_.move_to_element(page_selection).pause(1)
        actions_.double_click(page_selection).pause(1)
        actions_.send_keys(list(str(page_num))).pause(1)
        actions_.send_keys(list(Keys.ENTER)).pause(1)
        actions_.perform()

        print_method("move_to_page", f"page set to {page_num}!")

        self.check_page_loaded()

        self.get_page()

    @func_set_timeout(timeout=80)
    def set_preferences_to_all_information(self, close_bar: bool = False):
        """Activate the preference radio button 'all information'.

        Parameters
        ----------
        close_bar : bool, optional
            Close the bar after the preferences were set. The default is
            False.

        Returns
        -------
        None.
        """
        # The preferences need to only be set once per session. After they
        # have been set for the first time this function will immediately
        # return
        if self.preferences_set:
            return

        # First test whether the side-bar (called internally "infoSheet") is
        # currently active or not by trying to find it.
        try:
            self.driver.find_by_css("div[class*='layoutContentsCss']")
        except NoSuchElementException:
            # Only summon the info side-bar if it cannot be found.
            more_options_button = self.driver.wait_for_element_presence(
                "div > button:nth-child(2)"
            )
            more_options_button.click()
            sleep(2)

        # Element containing the 'advanced search' and 'prefences' tabs.
        tablist = self.driver.find_by_css("div[role='tablist']")

        # The "tabindex" value of the non-active tab always gets set to "-1"
        # by familysearch.
        preferences_tab = tablist.find_element(
            By.CSS_SELECTOR, "div[tabindex='-1']"
        )

        # Change to the preferences tab
        preferences_tab.click()
        sleep(1)

        # Make sure elements are fully loaded. There is a total of 7 radio
        # buttons.
        radio_buttons = WebDriverWait(self.driver, 90).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "input[type='radio']")
            )
        )

        # The fifth radio button is the one we are interested in.
        all_information_radio = radio_buttons[4]

        if not all_information_radio.is_selected():
            # Click the radio button
            all_information_radio.click()

            # Mark the preference as set
            self.preferences_set = True

            # NOTE: The "all_information" WebElement has become stale after
            # it was clicked upon previously. The WebElement needs to be
            # assigned again in order to avaoid a "stale" TypeError.
            all_information_radio = self.driver.find_all_by_css(
                "input[type='radio']"
            )[4]

            # Wait until the button has been activated
            WebDriverWait(self.driver, 90).until(
                EC.element_selection_state_to_be(all_information_radio, True)
            )
            sleep(1)

        # NOTE: The "tabindex" value of the non-active tab always gets set to
        # "-1" by familysearch.
        advanced_search_tab = tablist.find_element(
            By.CSS_SELECTOR, "div[tabindex='-1']"
        )

        # Change back to the advanced search tab
        advanced_search_tab.click()
        sleep(1)

        # Find and click on the close button in order to close the side-bar.
        # The try-statement prevents an exception should the close button
        # for some reason not exist.
        if close_bar:
            try:
                self.driver.find_button("button[aria-label='Close']")
            except NoSuchElementException:
                pass
