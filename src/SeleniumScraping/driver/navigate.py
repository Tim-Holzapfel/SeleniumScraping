"""Set number of records to show per page."""

# Future Implementations
from __future__ import annotations

# Standard Library
from configparser import ConfigParser
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING

# Thirdparty Library
import regex as re

from func_timeout import func_set_timeout
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Package Library
from SeleniumScraping.descriptors import (
    StrDesc,
    UserPassword,
    UserPath,
    UserProfiles,
)
from SeleniumScraping.driver.driverbase import DriverBase
from SeleniumScraping.driver.utils import (
    print_method,
    print_method_error,
    print_method_success,
)
from SeleniumScraping.exceptions import ProfileError


if TYPE_CHECKING:
    # Package Library
    from SeleniumScraping.base import TorBrowser


class Navigate(DriverBase):
    """Navigate Familysearch."""

    user_prof = UserProfiles()
    profile_path = UserPath("profile_path")
    user_name = StrDesc("user_name")
    user_password = UserPassword("user_password")
    css_class = "div[class*='layoutContentsCss']"

    def __init__(
        self,
        driver: TorBrowser,
    ) -> None:
        """Initiate navigation class.

        Parameters
        ----------
        driver : TorBrowser
            Modified Firefox browser routed through the onion network.
        """
        self.driver = driver
        self.pat_url = re.compile(r"cis-web\/oauth")
        super().__init__(driver)

    def load_profile(self) -> None:
        """Load user profile."""
        # Get next user profile path in the cycle
        self.profile_path = self.user_prof
        config = ConfigParser()
        config.read(self.profile_path)

        self.user_name = config["ACCOUNT"]["name"]
        self.user_password = config["ACCOUNT"]["password"]

    @func_set_timeout(timeout=80)
    def navigate_to_website_login(self) -> None:
        """Navigate to login page."""
        self.driver.delete_all_cookies()
        current_url = self.get_current_url()
        print_method(
            "navigate_to_website_login",
            "I'm waiting for the main page to load...",
        )
        self.driver.get("https://www.familysearch.org/en/")
        print_method_success(
            "navigate_to_website_login", "main page has fully loaded!"
        )
        del self.cycle_count

        while True:
            if self.cycle_count > 5:
                raise TimeoutError(
                    """navigate_to_website_login: Could not summong
                    sign in button!"""
                )
            try:

                self.click_consent_button()

                print_method(
                    "navigate_to_website_login",
                    """I'm waiting for the sign in button to
                    become clickable...""",
                )

                # Wait for sign in button to be clickable
                self.driver.find_button("a[href^='/auth/familysearch/']", 10)
                print_method_success(
                    "navigate_to_website_login",
                    "The sign in button was clicked!",
                )
                self.wait_for_url_change(current_url)
                break
            except TimeoutException:
                print_method_error(
                    "navigate_to_website_login",
                    """Trying to click on the Sign In button took too
                    long but I will try again.""",
                )
            except ElementClickInterceptedException:
                print_method_error(
                    "navigate_to_website_login",
                    """My click on the Sign In button got intercepted
                    but I will try again.""",
                )
                self.cycle_count += 1

    @func_set_timeout(timeout=80)
    def website_login(self) -> None:
        """Enter username and password for familysearch.org.

        Raises
        ------
        ProfileError
            If the profile was invalid.
        """
        # Load user credentials
        self.load_profile()
        # %% Enter credentials
        # Enter Username
        assert isinstance(self.user_name, str)
        print_method(
            "website_login",
            "I will try to enter the user name...",
        )

        # Entering user name
        self.driver.formfield_enter("input[name*='userName']", self.user_name)

        print_method_success(
            "website_login",
            "User Name entered!",
        )

        print_method(
            "website_login",
            "I will try to enter the user password...",
        )
        # Enter Password
        assert isinstance(self.user_password, str)
        self.driver.formfield_enter(
            "input[name*='password']", self.user_password
        )

        print_method_success(
            "website_login",
            "User Password entered!",
        )

        # Submit credentials
        print_method(
            "website_login",
            "I'm waiting for the website to respond to my login request...",
        )
        self.driver.find_button("#login", 10)

        # An error message will be displayed in case our credentials were
        # invalid. Otherwise, the page is going to change. The following loop
        # will repeatedly check if either the url has changed or if an error
        # is displayed: these two are usually the only possible events after
        # the "sign in" button was clicked.

        del self.cycle_count

        while True:

            if self.cycle_count > 5:
                raise TimeoutException("The website login took too long!")

            sleep(1)

            # Current browser url
            current_url = self.driver.current_url

            # bool to check if we are still on the login website
            auth_site = bool(self.pat_url.search(current_url))

            if not auth_site:
                print_method_success("website_login", "Login successful!")
                break
            try:
                self.driver.find_by_css("#errorAuthentication")
                prof_path = self.profile_path
                assert isinstance(prof_path, Path)
                prof_path.unlink()
                raise ProfileError(
                    "Current Profile was invalid and has been deleted."
                )
            except NoSuchElementException:
                print_method_error(
                    "website_login", "I'm still waiting for a response..."
                )
                self.cycle_count += 1

    @func_set_timeout(timeout=80)
    def navigate_to_search(self) -> None:
        """Navigate to the search tab of familysearch.org."""
        current_url = self.get_current_url()
        del self.cycle_count
        while True:
            if self.cycle_count > 5:
                raise TimeoutError(
                    "navigate_to_search: Could not move forward in time!"
                )
            try:
                # Click search button to summon submenu buttons
                self.driver.find_button("button[aria-controls='search']", 10)

                sleep(1)

                # The "records" search button element is as usual present but
                # invisible as long as the "main" search button has not been
                # clicked.
                WebDriverWait(
                    self.driver, timeout=15, poll_frequency=2
                ).until(
                    EC.visibility_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "li[class='submenu-item '] a[data-test='records']",
                        )
                    )
                ).click()
                print_method(
                    "navigate_to_search",
                    "search tab clicked!",
                )
                self.wait_for_url_change(current_url)
                break
            except TimeoutException:
                print_method_error(
                    "navigate_to_search",
                    """My search for the button timed out, I will
                    start looking for it again!""",
                )
                self.cycle_count += 1
            except ElementClickInterceptedException:
                print_method_error(
                    "navigate_to_search",
                    """My click got intercepted... I will try to
                    summon the navigate button again.""",
                )
                self.click_consent_button()
                self.survey_garbage()
                self.cycle_count += 1
                sleep(1)
            except NoSuchElementException:
                print_method_error(
                    "navigate_to_search",
                    """I couldn't find the navigate button... I will
                    try to summon the navigate button again.""",
                )
                self.cycle_count += 1
                sleep(1)
            except ElementNotInteractableException:
                print_method_error(
                    "navigate_to_search",
                    """I couldn't interact with the navigate button for some
                    reason... I will try to summon the navigate
                    button again.""",
                )
                self.click_consent_button()
                self.survey_garbage()
                self.cycle_count += 1
                sleep(1)

    @func_set_timeout(timeout=80)
    def navigate_to_records(self) -> None:
        """Navigate to the records tab of familysearch.org."""
        # For the page change indicator at the end of the page.

        current_url = self.get_current_url()

        # Enter query string to search for Mexico.
        print_method(
            "navigate_to_records",
            "I will try to enter the place name...",
        )
        self.driver.formfield_enter("#anyPlace", "Mexico", 0.6, True)
        print_method(
            "navigate_to_records", "name of the event place entered!"
        )

        self.wait_for_url_change(current_url)

        print_method("navigate_to_records", "I reached the main page!")
        self.check_page_loaded()

        # Set entries to show per page to 100
        print_method(
            "navigate_to_records",
            "I will try to set the records per page to 100...",
        )
        self.set_page_size()

    @func_set_timeout(timeout=80)
    def start_search_query(self, close_bar: bool = True) -> None:
        """Summon sidebar with advanced options."""
        # ---------- Assert That All Necessary Values Are Present ---------- #
        assert isinstance(
            self.event_country, str
        ), "start_search_query: event_country is not set!"
        assert isinstance(
            self.event_state, str
        ), "start_search_query: event_state is not set!"
        assert isinstance(
            self.event_munic, str
        ), "start_search_query: event_munic is not set!"
        assert isinstance(
            self.year_to, int
        ), "start_search_query: year_to is not set!"
        assert isinstance(
            self.year_from, int
        ), "start_search_query: year_from is not set!"

        # First test whether the side-bar (called internally "infoSheet") is
        # currently active or not by trying to find it.
        try:
            info_sheet_table = self.driver.find_by_css(self.css_class)
        except NoSuchElementException:
            # Only summon the info side-bar if it cannot be found.
            more_options_button = self.driver.wait_for_element_presence(
                "div > button:nth-child(2)"
            )
            more_options_button.click()
            sleep(2)

        # Find element containing the "death button"
        death_button = self.driver.find_element(By.NAME, "Death-chip")

        del self.cycle_count

        # Only click the "death button" if it has not already been clicked.
        # Should the "death button" not be clickable then it's likely
        # because we are not up enough on the website. Hence, in case of
        # an ElementClickInterceptedException we need to go up the website.
        if not death_button.is_selected():
            while True:
                if self.cycle_count > 2:
                    raise WebDriverException
                try:
                    death_button.click()
                    sleep(2)
                    break
                except ElementClickInterceptedException:
                    info_sheet_table = self.driver.find_by_css(self.css_class)
                    website_root = self.driver.find_by_css(":root")

                    info_sheet_table.send_keys(list(Keys.PAGE_UP))
                    sleep(1)

                    website_root.send_keys(list(Keys.PAGE_UP))

                    sleep(1.5)
                    self.cycle_count += 1

        query_str = ", ".join(
            [self.event_munic, self.event_state, self.event_country]
        )

        # Enter the query string into the formfield
        self.driver.formfield_enter(
            "input[name*='deathLikePlace']", query_str
        )

        # Enter starting date for deathyear
        self.driver.formfield_enter(
            "input[name*='q_deathLikeDate_from']", self.year_from
        )

        # Enter ending date for deathyear
        self.driver.formfield_enter(
            "input[name*='q_deathLikeDate_to']", self.year_to
        )

        # Test if there are currently any buttons other than the "death
        # button" (which has the label "REMOVE DEATH EVENT") is currently
        # displayed
        remove_event_buttons = self.driver.find_all_by_css(
            "button[aria-label^='Remove' i]:not([aria-label*='Death' i])"
        )

        # Clicking the button is not always directly possible because the
        # search button at the end of the page is a "floating" type, meaning
        # the search button is always visible which can mean that the element
        # of the search button can obscure the button we are trying to click.
        # Should that be the then we can try to scroll down the page in order
        # to reach the button.
        del self.cycle_count
        if len(remove_event_buttons) > 0:
            for button_ in remove_event_buttons:
                while True:
                    if self.cycle_count > 2:
                        raise WebDriverException
                    try:
                        button_.click()
                        sleep(1.5)
                        break
                    except ElementClickInterceptedException:
                        info_sheet_table = self.driver.find_by_css(
                            self.css_class
                        )
                        if self.cycle_count % 2 != 0:
                            info_sheet_table.send_keys(list(Keys.PAGE_DOWN))
                        else:
                            info_sheet_table.send_keys(list(Keys.PAGE_UP))

                        sleep(1.5)
                        self.cycle_count += 1

        # Find and click on the search button (blue button with a magnifying
        # glass icon)
        self.driver.find_button(
            "div.css-nzy20i-bleedCss > div > div > button:nth-child(1)"
        )

        self.botcheck_test()

        # Waiting for the page to be loaded
        self.check_page_loaded()

        # Find and click on the close button in order to close the side-bar
        # but only if the search returned results. Otherwise it makes no
        # sense to close the bar because we would need to repopen it
        # immediately.
        if close_bar and not self.no_results_found:
            self.driver.find_button("button[aria-label='Close']")
