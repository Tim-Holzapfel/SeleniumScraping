"""Driver on which all of the package builds."""

# Future Implementations
from __future__ import annotations

# Standard Library
from dataclasses import asdict, dataclass
from os import devnull
from time import sleep

# Thirdparty Library
import pandas as pd
import regex as re

from func_timeout import func_set_timeout
from furl import furl
from selenium.common.exceptions import ElementNotSelectableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.webdriver import (
    FirefoxProfile,
    WebDriver as Firefox,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Package Library
from SeleniumScraping.driver.utils import java_kill, start_tor, wait_dist
from SeleniumScraping.filepaths import FilePaths


# -------------------------------------------------------------------------- #
#                                 Tor Driver                                 #
# -------------------------------------------------------------------------- #


class TorBrowser(Firefox):
    """Start Tor Browser.

    Generate a Firefox Browser while routing traffic through Tor.


    Attributes
    ----------
    tor_exe

    Methods
    -------
    find_by_css():
    find_all_by_css(css_selector):
        Prints the person's name and age.
    close_browser():
    wait_for_element_presence():
    wait_for_element_clickable():
    find_button(css_selector, selector_type):
        Find button using selector and click it.
    formfield_enter():
        Simulate user presence while interacting with formfields.
    get_sms():
    """

    def __init__(
        self,
        headless: bool = False,
        onion_network: bool = True,
        dev_mode: bool = False,
    ) -> None:
        """Start a Firefox marionette and route traffic through Tor.

        Parameters
        ----------
        headless : bool, optional
            Start the browser with a Graphical User Interface (GUI).
            The default is False.
        onion_network : bool, optional
            Route the in- and outgoing traffic through the onion network.
            The default is True.
        dev_mode : bool, optional
            Use the development mode. The default is False.
        """
        self.headless = headless
        self.onion_network = onion_network
        # Enter development mode
        if dev_mode:
            self.headless = True
            self.onion_network = False

        profile = FirefoxProfile()
        options = FirefoxOptions()
        options.headless = self.headless
        options.accept_insecure_certs = True

        if self.onion_network:
            self.tor_exe = start_tor(t_max=80)
            browser_prefs = replace_keys(Settings())
            options.preferences.update(browser_prefs)
            profile.default_preferences.update(browser_prefs)

        super().__init__(
            firefox_profile=profile,
            options=options,
            executable_path=FilePaths.geckodriver_path.as_posix(),
            service_log_path=devnull,
        )

        self.maximize_window()

        self.delete_all_cookies()

    @func_set_timeout(timeout=80)
    def close_browser(self) -> None:
        """Close the Browser."""
        # Close driver window
        self.close()
        sleep(1)
        java_kill()
        if self.onion_network:
            # Terminate the tor exe
            self.tor_exe.terminate()
            sleep(1)
            # Kill all process related to the driver to make sure it is closed
            java_kill()

    @func_set_timeout(timeout=80)
    def find_by_css(self, css_value: str) -> WebElement:
        """Find webelement by css selector.

        Parameters
        ----------
        css_value : str
            CSS locator string.

        Returns
        -------
        WebElement
        """
        return self.find_element(by=By.CSS_SELECTOR, value=css_value)

    @func_set_timeout(timeout=80)
    def find_all_by_css(self, css_value: str) -> list[WebElement]:
        """Find all webelement by css selector.

        Parameters
        ----------
        css_value : str
            CSS locator string.

        Returns
        -------
        List[WebElement]
        """
        return self.find_elements(by=By.CSS_SELECTOR, value=css_value)

    @func_set_timeout(timeout=80)
    def wait_for_element_presence(
        self, css_value: str, timeout_secs: int = 90
    ) -> WebElement:
        """Wait for the presence of the element to be located.

        Parameters
        ----------
        css_value : str
            CSS locator string.
        timeout_secs : int, optional
            Seconds until a timeout exception is raised. The default is 90.

        Raises
        ------
        TimeoutException
            If the element could not be located within the given timeframe.

        Returns
        -------
        WebElement
        """
        return WebDriverWait(self, timeout_secs).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_value))
        )

    @func_set_timeout(timeout=80)
    def wait_for_element_clickable(
        self, css_value: str, timeout_secs: int = 90
    ) -> WebElement:
        """Wait for the element to be clickable.

        Parameters
        ----------
        css_value : str
            CSS locator string.
        timeout_secs : int, optional
            Seconds until a timeout exception is raised. The default is 90.

        Raises
        ------
        TimeoutException
            If the element could not be located within the given timeframe.

        Returns
        -------
        WebElement
        """
        return WebDriverWait(self, timeout_secs).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_value))
        )

    @func_set_timeout(timeout=80)
    def find_button(
        self, css_selector: str, timeout_secs: int = 90
    ) -> WebElement:
        """Find button using CSS selector and click it.

        Parameters
        ----------
        css_value : str
            CSS locator string.
        timeout_secs : int, optional
            Seconds until a timeout exception is raised. The default is 90.

        Raises
        ------
        TimeoutException
            If the element could not be located within the given timeframe.

        Returns
        -------
        WebElement
        """
        button_field = self.wait_for_element_clickable(
            css_selector, timeout_secs
        )

        button_field.click()

        return button_field

    @func_set_timeout(timeout=80)
    def formfield_enter(
        self,
        locater: str,
        field_value: str | int,
        mean_wait: int | float = 0.2,
        list_selection: bool = False,
    ) -> WebElement:
        """Enter value into a formfield.

        Parameters
        ----------
        locater : str
            CSS locator string.
        field_value : str, int
            String or integer to send to the formfield.
        mean_wait : int, float, optional
            Time to wait (on average) before sending another keystroke to the
            formfield. The default is 0.2.
        list_selection : bool, optional
            Expect a list-like field to appear and act accordingly.
            The default is False.

        Returns
        -------
        WebElement
        """
        # Element containing the text string of the formfield and obtaining
        # the current value (property value).

        # Element containing the year formfield
        formfield_element = self.wait_for_element_clickable(locater)

        # Current value of the formfield (property: value displayed in the
        # formfield)
        formfield_value = formfield_element.get_property("value")

        # If the value to be entered is already present in the formfield
        # then return
        if formfield_value == str(field_value):
            return formfield_element

        # Initialize the action chain operator
        action_ = ActionChains(self)

        action_.move_to_element(formfield_element)

        # try to delete the current element (if existent) first by simply
        # removing it and, should that not work, by "manually" double clicking
        # and pressing the "DELETE" button.

        try:
            # Try to clear any possibly existing values from the formfield
            # first the "conventional" way.
            formfield_element.clear()
            action_.click(formfield_element).pause(1)
        except ElementNotSelectableException:
            # Double click to select whole field
            action_.double_click(formfield_element).pause(1)

            # Press "delete" button to remove any string possibly present.
            action_.send_keys(list(Keys.DELETE))

        # Array same length as `formfield_value` where each element of the
        # array corresponds to the time in seconds to wait for the respective
        # letter of `formfield_value`.
        input_delay = wait_dist(field_value, mean_wait)

        for idx, i in enumerate(str(field_value)):
            action_.send_keys(list(i)).pause(input_delay[idx])

        url_excep = (
            furl(self.current_url).pathstr
            == "/cis-web/oauth2/v3/authorization"
        )

        # Sometimes the targeted formfield will open a list with suggestions
        # based on the current formfield value. However, this feature seems to
        # be actively developed at the moment and is currently not
        # operational.

        # The only time where this will never happen is of course the sign in
        # page because of the uniqueness of user names an autosuggestion is
        # not possible and also of course in cases where an integer or float
        # value needs to be entered (like for years for example).

        # list_selection should be set to False if this feature is currently
        # not working and to True when it is.
        if list_selection and isinstance(field_value, str) and not url_excep:
            sleep(10)
            # action_.send_keys(list(Keys.ARROW_DOWN)).pause(10)
            action_.send_keys(list(Keys.ENTER)).pause(2)

        action_.perform()

        return formfield_element

    @func_set_timeout(timeout=80)
    def get_sms(self) -> None:
        """Scrape receive-smss.com for SMS numbers."""
        self.get("https://receive-smss.com/")

        # %% Generate DataFrame
        sms_df = pd.DataFrame(columns=["sms_number", "sms_country"])
        sms_df.reset_index(drop=True, inplace=True)

        sms_number = self.find_all_by_css(
            "div[class^='number-boxes-item'][class$='flex-column '] h4[class$='number']"
        )

        sms_country = self.find_all_by_css(
            "div[class^='number-boxes-item'][class$='flex-column '] h5[class$='country']"
        )

        for _number, _country in zip(sms_number, sms_country):
            # Familysearch seems to put more scrutiny on US phone numbers, for
            # example they will complain if an US phone number was used more
            # than once but don't seem to care if e.g. a German phone number
            # was used more than once.
            if _country.text != "United States":
                sms_df.loc[len(sms_df)] = {
                    "index": len(sms_df),
                    "sms_number": _number.text,
                    "sms_country": _country.text,
                }

        sms_df.to_feather(path=FilePaths.sms_df_user)


def replace_keys(input_data: Settings) -> dict[str, int | str | bool]:
    """Replace dictionary keys.

    Parameters
    ----------
    input_data : Settings
        Instance of Settings dataclass.

    Returns
    -------
    output_dict : dict
        Dictionary constructed from input.
    """
    input_dict: dict[str, int | str | bool] = asdict(input_data)
    output_dict = {re.sub("__", "-", k): v for k, v in input_dict.items()}
    output_dict = {re.sub("_", ".", k): v for k, v in output_dict.items()}
    return output_dict


@dataclass
class Settings(object):
    """Browser Settings to assure privacy."""

    app_shield_optoutstudies_enabled: bool = True
    app_update_BITS_enabled: bool = False
    app_update_auto_migrated: bool = False
    app_update_background_experimental: bool = False
    app_update_background_scheduling_enabled: bool = False
    app_update_service_enabled: bool = False
    beacon_enabled: bool = False
    browser_cache_disk_enable: bool = True
    browser_cache_disk_cache_ssl: bool = True
    browser_cache_memory_enable: bool = True
    browser_cache_offline_enable: bool = False
    browser_display_show_image_placeholders: bool = False
    browser_formfill_enable: bool = False
    browser_privatebrowsing_autostart: bool = True
    browser_safebrowsing_downloads_enabled: bool = False
    browser_safebrowsing_downloads_remote_url: str = ""
    browser_safebrowsing_enabled: bool = False
    browser_safebrowsing_malware_enabled: bool = False
    browser_safebrowsing_phishing_enabled: bool = False
    browser_safebrowsing_provider_google_advisoryURL: str = ""
    browser_safebrowsing_provider_google_gethashURL: str = ""
    browser_safebrowsing_provider_google_lists: str = ""
    browser_safebrowsing_provider_google_pver: str = ""
    browser_safebrowsing_provider_google_reportMalwareMistakeURL: str = ""
    browser_safebrowsing_provider_google_reportPhishMistakeURL: str = ""
    browser_safebrowsing_provider_google_reportURL: str = ""
    browser_safebrowsing_provider_google_updateURL: str = ""
    browser_safebrowsing_provider_google4_advisoryName: str = ""
    browser_safebrowsing_provider_google4_advisoryURL: str = ""
    browser_safebrowsing_provider_google4_dataSharing_enabled: str = ""
    browser_safebrowsing_provider_google4_dataSharingURL: str = ""
    browser_safebrowsing_provider_google4_gethashURL: str = ""
    browser_safebrowsing_provider_google4_lists: str = ""
    browser_safebrowsing_provider_google4_reportMalwareMistakeURL: str = ""
    browser_safebrowsing_provider_google4_reportPhishMistakeURL: str = ""
    browser_safebrowsing_provider_google4_reportURL: str = ""
    browser_safebrowsing_provider_google4_updateURL: str = ""
    browser_search_geoip_url: str = ""
    browser_search_suggest_enabled: bool = False
    browser_selfsupport_url: bool = False
    browser_send_pings: bool = False
    browser_tabs_disableBackgroundZombification: bool = True
    browser_tabs_loadInBackground: bool = False
    browser_zoom_updateBackgroundTabs: bool = False
    browserName: str = "firefox"
    doh__rollout_home__region: str = "US"
    dom_battery_enabled: bool = False
    dom_event_clipboardevents_enabled: bool = False
    extensions_autoDisableScopes: int = 0
    extensions_enabledScopes: int = 15
    extensions_systemAddon_update_enabled: bool = False
    extensions_webextensions_background__delayed__startup: bool = False
    general_useragent_locale: str = "en-US"
    geo_enabled: bool = False
    geo_wifi_uri: str = ""
    javascript: bool = True
    media_peerconnection_enabled: bool = False
    network_IDN_show_punycode: bool = True
    network_cookie_cookieBehavior: int = 1
    network_dns_disablePrefetch: bool = True
    network_dns_disablePrefetchFromHTTPS: bool = True
    network_http_speculative__parallel__limit: int = 0
    network_http_use__cache: bool = False
    network_predictor_enable__prefetch: bool = False
    network_prefetch__next: bool = False
    network_proxy_socks: str = "127_0_0_1"
    network_proxy_socks_port: int = 9150
    network_proxy_socks_remote_dns: bool = True
    network_proxy_socks_version: int = 5
    network_proxy_type: int = 1
    network_websocket_enabled: bool = False
    permissions_default_geo: int = 2
    permissions_default_image: int = 2
    places_history_enabled: bool = False
    plugin_scan_plid_all: bool = False
    plugin_state_flash: int = 0
    port: int = 4444
    privacy_antitracking_testing: bool = True
    privacy_clearOnShutdown_history: bool = True
    privacy_clearOnShutdown_offlineApps: bool = True
    privacy_clearOnShutdown_openWindows: bool = True
    privacy_clearOnShutdown_siteSettings: bool = True
    privacy_cpd_cache: bool = False
    privacy_cpd_cookies: bool = False
    privacy_cpd_history: bool = False
    privacy_donottrackheader_enabled: bool = True
    privacy_firstparty_isolate: bool = True
    privacy_partition_network_state_connection_with_proxy: bool = True
    privacy_purge_trackers_enabled: bool = True
    privacy_resistFingerprinting: bool = True
    privacy_sanitize_sanitizeOnShutdown: bool = True
    privacy_spoof_english: int = 1
    privacy_trackingprotection_enabled: bool = True
    privacy_trackingprotection_lower_network_priority: bool = True
    remoteServerAddr: str = "localhost"
    services_sync_engine_history: bool = False
    services_sync_prefs_sync_browser_startup_homepage: bool = False
    toolkit_legacyUserProfileCustomizations_stylesheets: bool = True
    xpinstall_signatures_required: bool = False
