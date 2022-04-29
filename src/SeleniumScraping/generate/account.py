"""Scrape familysearch."""

# Future Implementations
from __future__ import annotations

# Standard Library
from configparser import ConfigParser
from pathlib import Path
from shutil import copy2
from time import sleep

# Thirdparty Library
import pandas as pd
import regex as re

from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.descriptors import (
    BoolDescriptor,
    ProfIter,
    StrDesc,
    UserPassword,
    UserPath,
)
from SeleniumScraping.driver.driverbase import DriverBase
from SeleniumScraping.driver.utils import (
    print_method,
    print_method_error,
    print_method_success,
)
from SeleniumScraping.exceptions import (
    NoFlagFoundError,
    NoSMSCodeError,
    ProfileError,
)
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.generate.utils import expand_se


class RegisterUser(DriverBase):
    """Activate user profile."""

    def __init__(self, driver: TorBrowser, driver_sms: TorBrowser):
        """Initialize class."""
        self.driver = driver
        self.driver_sms = driver_sms
        self.fs_pat = re.compile(
            r"(?<=Your FamilySearch verification code is ).*(?=\.)"
        )
        super().__init__(driver)

    # Boolean Descriptors
    consent_button_clicked = BoolDescriptor("consent_button_clicked")

    prof_iter = ProfIter()
    profile_path = UserPath("profile_path")
    first_name = StrDesc("first_name")
    last_name = StrDesc("last_name")
    user_gender = StrDesc("user_gender")
    year_birth = StrDesc("year_birth")
    month_birth_int = StrDesc("month_birth_int")
    month_birth_chr = StrDesc("month_birth_chr")
    day_birth = StrDesc("day_birth")
    sms_number = StrDesc("sms_number")
    sms_country = StrDesc("sms_country")
    user_password = UserPassword("user_password")
    user_account_name = StrDesc("user_account_name")
    phone_website = StrDesc("phone_website")

    def reset_descriptors(self):
        del self.consent_button_clicked

    def read_profile(self):
        """Read user information from configuration file."""
        self.profile_path = self.prof_iter

        config = ConfigParser()
        config.read(self.profile_path)

        self.first_name = config["USER"]["first_name"]
        self.last_name = config["USER"]["last_name"]
        self.user_gender = config["USER"]["gender"]
        self.year_birth = config["USER"]["year_birth"]
        self.month_birth_int = config["USER"]["month_birth_int"]
        self.month_birth_chr = config["USER"]["month_birth_chr"]
        self.day_birth = config["USER"]["day_birth"]
        self.sms_number = config["PHONE"]["phone_number"]
        self.sms_country = config["PHONE"]["phone_country"]
        self.user_password = config["ACCOUNT"]["password"]
        self.user_account_name = config["ACCOUNT"]["name"]
        self.phone_website = config["PHONE"]["phone_website"]

    def move_user_profile(self):
        """Mark current profile as active."""
        assert isinstance(self.profile_path, str)
        profile_path = Path(self.profile_path)

        config = ConfigParser()
        config.read(profile_path)

        config["ACCOUNT"]["activated"] = "True"

        with open(profile_path, "w", encoding="UTF-8") as configfile:
            config.write(configfile)

        copy2(profile_path, FilePaths.active_profs_dir_user)

        profile_path.unlink()

    def first_page(self):
        """Navigate to first page and enter necessary information."""
        # Bring driver into focus
        self.driver.minimize_window()
        self.driver.maximize_window()

        self.driver.get("https://www.familysearch.org/register/custom/1")

        self.click_consent_button()

        # First name of user
        assert isinstance(self.first_name, str)
        self.driver.formfield_enter(
            "input[name='firstName']", self.first_name
        )

        sleep(1)

        # Last name of user
        print_method(
            "first_page", "I will try to enter the first name of the user..."
        )
        assert isinstance(self.last_name, str)
        self.driver.formfield_enter("input[name='lastName']", self.last_name)
        print_method_success("first_page", "First name entered successfully!")

        sleep(1)

        # Month of birth of user
        print_method(
            "first_page",
            "I will try to select the birth month of the user...",
        )
        assert isinstance(self.month_birth_chr, str)
        Select(
            self.driver.find_by_css("select[name='registerMonth']")
        ).select_by_visible_text(self.month_birth_chr)
        print_method_success(
            "first_page", "Birth month selected successfully!"
        )

        sleep(1)

        # Day of birth of user
        print_method(
            "first_page", "I will try to select the birth day of the user..."
        )
        assert isinstance(self.day_birth, str)
        Select(
            self.driver.find_by_css("select[name='registerDay']")
        ).select_by_visible_text(self.day_birth)
        print_method_success("first_page", "Birth day selected successfully!")
        sleep(1)

        # Year of birth of user
        print_method(
            "first_page", "I will try to select the birth year of the user..."
        )
        assert isinstance(self.year_birth, str)
        Select(
            self.driver.find_by_css("select[name='registerYear']")
        ).select_by_visible_text(self.year_birth)
        print_method_success(
            "first_page", "Birth year selected successfully!"
        )
        sleep(1)

        # User gender
        print_method("first_page", "I will try to select the user gender...")
        self.driver.find_by_css(f"label[for='{self.user_gender}']").click()
        print_method_success(
            "first_page", "User gender selected successfully!"
        )
        sleep(1)

        # Continue button
        self.driver.find_button("button[data-test*='continue']")

    def second_page(self):
        """Navigate to second page and supply required information."""
        # User account name
        assert isinstance(self.user_account_name, str)
        self.driver.formfield_enter("#username", self.user_account_name)

        sleep(1)

        # Test if username error field is displayed
        # NOTE: The username error element itself is always present but
        # only displayed if an error occurs.
        username_error = WebDriverWait(
            self.driver, timeout=15, poll_frequency=2
        ).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#username-taken")
            )
        )

        if username_error.is_displayed():
            print_method_error(
                "second_page",
                "Username was already taken! Continuing to next profile.",
            )
            # Delete profile with invalid name
            assert isinstance(self.profile_path, str)
            Path(self.profile_path).unlink()
            raise ProfileError

        # User account password
        print_method(
            "second_page", "I will try to enter the user account password..."
        )
        assert isinstance(self.user_password, str)
        self.driver.formfield_enter("#registerPassword", self.user_password)
        print_method_success(
            "second_page", "User account password entered successfully!"
        )
        sleep(1)

        # User account password confirmation
        print_method(
            "second_page",
            "I will try to enter the user account password a second time for confirmation...",
        )
        assert isinstance(self.user_password, str)
        self.driver.formfield_enter(
            "#registerPasswordConfirm", self.user_password
        )
        print_method_success(
            "second_page",
            "User account password entered successfully a second time!",
        )
        sleep(1)

        # %% SMS flag selection
        sms_flags = self.driver.find_by_css("#register-sms")

        try:
            sms_shadow = expand_se(self.driver, sms_flags)[1]
        except JavascriptException as java_exc:
            print_method_error(
                "second_page",
                "The country flag symbol did not appear for some reason...",
            )
            raise NoFlagFoundError from java_exc

        # Click to summon country list element. The country list needs
        # to be open in order for us to be able to select a country
        sms_shadow.find_element(By.CSS_SELECTOR, "#showList").click()

        sleep(1)

        sms_co_list = sms_shadow.find_elements(
            By.CSS_SELECTOR, "#list li .country-value"
        )

        country_name_list = [
            country_name.text for country_name in sms_co_list
        ]

        assert isinstance(self.sms_country, str)
        idx_co = country_name_list.index(self.sms_country)

        # Select country by flag
        sms_co_list[idx_co].click()

        sleep(1)

        # SMS number formfield
        assert isinstance(self.sms_number, str)
        self.driver.formfield_enter("#sms", self.sms_number)

        sleep(1)

        # %% Country list
        Select(self.driver.find_by_css("#country")).select_by_visible_text(
            self.sms_country
        )

        sleep(1)

        # %% Terms and conditions checkbox

        self.driver.find_by_css("label[for='terms']").click()

        sleep(1)

        # %% Submit button

        self.driver.find_by_css("button[type='submit']").click()

        # Waiting for the arrival of the SMS confirmation code
        assert isinstance(self.phone_website, str)
        sms_code = self.get_sms_code(self.phone_website)

        self.driver.minimize_window()
        self.driver.maximize_window()

        # Entering validation Code that we received by SMS
        self.driver.formfield_enter("#sms-token", sms_code)

        # Click submit button
        self.driver.find_button("button[ng-click='verifySMS(token)']")

        # Waiting for "Thank You!" message to make sure that the account was
        # successfully activated
        fs_msg = self.driver.wait_for_element_presence(
            "h1[class$='validate-heading']"
        )

        if fs_msg.text == "Thank You!":
            print_method("second_page", "Account activation successful!!")
            self.move_user_profile()

        self.driver.close_browser()

    def get_sms_code(self, phone_website: str) -> str:
        """Get activation code."""
        self.driver_sms.minimize_window()
        self.driver_sms.maximize_window()

        self.driver_sms.get(phone_website)

        times_refreshed = 0
        max_tries = 6
        while True:
            tbody = self.driver_sms.find_by_css("tbody")

            table_row = tbody.find_elements(By.CSS_SELECTOR, "tr")
            elements_searched = 0
            for table_cell in table_row:
                elements_searched += 1
                _cell = table_cell.find_element(
                    By.CSS_SELECTOR, ":nth-child(4)"
                )

                _match = self.fs_pat.search(_cell.text)

                if _match is not None:
                    print_method(
                        "get_sms_code", "I found the SMS from Familysearch!"
                    )
                    return _match.group(0)
                if elements_searched >= 6:
                    times_refreshed += 1
                    if times_refreshed > 6:
                        print_method(
                            "get_sms_code",
                            """It seems that Familysearch didn't send a message.
                            I will stop looking, delete the profile and put
                            the current phone number on the SMS blacklist file.""",
                        )

                        blacklist_df = pd.read_feather(
                            FilePaths.blacklist_path
                        )
                        blacklist_df.loc[len(blacklist_df) + 1] = {
                            "sms_number": self.sms_number,
                            "sms_country": self.sms_country,
                        }
                        blacklist_df.drop_duplicates(inplace=True)
                        blacklist_df.reset_index(drop=True, inplace=True)
                        blacklist_df.to_feather(FilePaths.blacklist_path)

                        # Delete profile
                        assert isinstance(self.profile_path, str)
                        Path(self.profile_path).unlink()

                        raise NoSMSCodeError
                    print_method(
                        "get_sms_code",
                        f"SMS from Familysearch not found. I will refresh the browser and start the search again (try {times_refreshed} of {max_tries}).",
                    )
                    self.driver_sms.refresh()

                    break
                sleep(2)
