"""Safeguards against various botchecks."""

# Future Implementations
from __future__ import annotations

# Standard Library
from time import sleep

# Thirdparty Library
from func_timeout import func_set_timeout
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.descriptors import (
    BoolDescriptor,
    CountryISO,
    CycleCount,
    EventCountry,
    EventPlace,
    EventYear,
    PageNumber,
)
from SeleniumScraping.driver.utils import (
    Messages,
    print_method,
    print_method_error,
    print_method_success,
)


class SafeGuards(object):
    """Scraping safeguards."""

    # Boolean Descriptors
    consent_button_clicked = BoolDescriptor("consent_button_clicked")
    preferences_set = BoolDescriptor("preferences_set")
    survey_popup_clicked = BoolDescriptor("survey_popup_clicked")
    keep_in_touch_popup_clicked = BoolDescriptor(
        "keep_in_touch_popup_clicked"
    )

    # Place related descriptors
    event_country = EventCountry("event_country")
    event_munic = EventPlace("event_munic")
    event_state = EventPlace("event_state")
    country_iso = CountryISO("country_iso")

    # Page related descriptors
    no_results_found = BoolDescriptor("no_results_found")
    page = PageNumber("page")
    page_max = PageNumber("page_max")

    # Year related descriptors
    year_from = EventYear("year_from")
    year_to = EventYear("year_to")

    # Misc descriptors
    cycle_count = CycleCount("cycle_count")
    botcheck_msg = Messages()

    def __init__(self, driver: TorBrowser) -> None:
        """Scraping safeguards."""
        self.driver = driver

    def reset_descriptors(self) -> None:
        """Reset descriptors."""
        # Boolean Descriptors
        del self.consent_button_clicked
        del self.preferences_set
        del self.survey_popup_clicked
        del self.keep_in_touch_popup_clicked

        # Place related descriptors
        del self.event_country
        del self.event_munic
        del self.event_state
        del self.country_iso

        # Page related descriptors
        del self.no_results_found
        del self.page
        del self.page_max

        # Year related descriptors
        del self.year_from
        del self.year_to

    @func_set_timeout(timeout=80)
    def survey_garbage(self) -> None:
        """Decline the survey popup if it should appear."""
        if self.survey_popup_clicked and self.keep_in_touch_popup_clicked:
            return
        if not self.survey_popup_clicked:
            try:
                self.driver.find_button(
                    "button[class*='QSIWebResponsiveDialog']:nth-child(2)", 4
                )
                self.survey_popup_clicked = True
                print_method_success(
                    "survey_garbage",
                    "The survey banner appeared but I could click it away!",
                )
            except TimeoutException:
                pass
        if not self.keep_in_touch_popup_clicked:
            try:
                self.driver.find_button("#gdprStopEmails", 4)
                self.keep_in_touch_popup_clicked = True
                print_method_success(
                    "survey_garbage",
                    "The 'keep in touch' banner appeared but I could click it away!",
                )
            except TimeoutException:
                sleep(0.5)

    @func_set_timeout(timeout=80)
    def botcheck_test(self):
        """Check if a botcheck has been invoked by familysearch."""
        del self.cycle_count
        while True:
            if self.cycle_count > 3:
                raise ValueError
            try:
                # Results error
                self.driver.find_by_css("div[data-testid='resultsError']")
                self.botcheck_msg = [self.cycle_count, "positive"]
                self.botcheck_msg  # pylint: disable=pointless-statement
                self.driver.refresh()
                sleep(3)
                self.cycle_count += 1
            except NoSuchElementException:
                pass
            try:
                # Results error
                self.driver.find_by_css(
                    "div[data-testid='tryYourSearchAgain'] h4"
                )
                self.botcheck_msg = [self.cycle_count, "positive"]
                self.botcheck_msg  # pylint: disable=pointless-statement
                self.driver.refresh()
                sleep(3)
                self.cycle_count += 1
            except NoSuchElementException:
                if self.cycle_count > 1:
                    self.botcheck_msg = [self.cycle_count, "negative"]
                    self.botcheck_msg  # pylint: disable=pointless-statement
                break

    @func_set_timeout(timeout=80)
    def click_consent_button(self) -> None:
        """Find and click on consent button."""
        if not self.consent_button_clicked:
            try:
                print_method(
                    "navigate_to_website_login",
                    "I'm waiting for the 'click-consent' popup to appear...",
                )

                self.driver.find_button("button#truste-consent-button", 5)

                WebDriverWait(self.driver, 90).until(
                    EC.invisibility_of_element(
                        (By.CSS_SELECTOR, "button#truste-consent-button")
                    )
                )

                self.consent_button_clicked = True
                print_method_success(
                    "click_consent_button", "consent button clicked!"
                )
            except TimeoutException:
                print_method_error(
                    "click_consent_button", "consent button did not appear!"
                )

    @func_set_timeout(timeout=80)
    def detect_iframe(self) -> None:
        """Test if the overlay if blocked by an iframe."""
        try:
            iframe_css = self.driver.find_by_css(
                ".usabilla_scroller_area > div:nth-child(1) > iframe:nth-child(1)"
            )

            self.driver.switch_to_frame(iframe_css)

            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()

            self.driver.switch_to_default_content()
        except NoSuchElementException:
            pass
