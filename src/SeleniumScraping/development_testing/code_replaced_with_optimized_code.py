

class BrowserSettings:
    """Firefox settings to assure anonymity."""

    def __init__(self) -> None:
        """Firefox settings to assure anonymity."""
        self.browser = "Firefox"

    @staticmethod
    def get_settings() -> dict[str, str | int | bool]:
        """Retrieve Browser settings."""
        return dict(
            {
                "app.shield.optoutstudies.enabled": True,
                "app.update.BITS.enabled": False,
                "app.update.auto.migrated": False,
                "app.update.background.experimental": False,
                "app.update.background.scheduling.enabled": False,
                "app.update.service.enabled": False,
                "beacon.enabled": False,
                "browser.cache.disk.enable": True,
                "browser.cache.disk_cache_ssl": True,
                "browser.cache.memory.enable": True,
                "browser.cache.offline.enable": False,
                "browser.display.show_image_placeholders": False,
                "browser.formfill.enable": False,
                "browser.privatebrowsing.autostart": True,
                "browser.safebrowsing.downloads.enabled": False,
                "browser.safebrowsing.downloads.remote.url": "",
                "browser.safebrowsing.enabled": False,
                "browser.safebrowsing.malware.enabled": False,
                "browser.safebrowsing.phishing.enabled": False,
                "browser.safebrowsing.provider.google.advisoryURL": "",
                "browser.safebrowsing.provider.google.gethashURL": "",
                "browser.safebrowsing.provider.google.lists": "",
                "browser.safebrowsing.provider.google.pver": "",
                "browser.safebrowsing.provider.google.reportMalwareMistakeURL": "",
                "browser.safebrowsing.provider.google.reportPhishMistakeURL": "",
                "browser.safebrowsing.provider.google.reportURL ": "",
                "browser.safebrowsing.provider.google.updateURL": "",
                "browser.safebrowsing.provider.google4.advisoryName": "",
                "browser.safebrowsing.provider.google4.advisoryURL": "",
                "browser.safebrowsing.provider.google4.dataSharing.enabled": "",
                "browser.safebrowsing.provider.google4.dataSharingURL": "",
                "browser.safebrowsing.provider.google4.gethashURL": "",
                "browser.safebrowsing.provider.google4.lists": "",
                "browser.safebrowsing.provider.google4.reportMalwareMistakeURL": "",
                "browser.safebrowsing.provider.google4.reportPhishMistakeURL": "",
                "browser.safebrowsing.provider.google4.reportURL": "",
                "browser.safebrowsing.provider.google4.updateURL": "",
                "browser.search.geoip.url": "",
                "browser.search.suggest.enabled": False,
                "browser.selfsupport.url": False,
                "browser.send_pings": False,
                "browser.tabs.disableBackgroundZombification": True,
                "browser.tabs.loadInBackground": False,
                "browser.zoom.updateBackgroundTabs": False,
                "browserName": "firefox",
                "doh-rollout.home-region": "US",
                "dom.battery.enabled": False,
                "dom.event.clipboardevents.enabled": False,
                "extensions.autoDisableScopes": 0,
                "extensions.enabledScopes": 15,
                "extensions.systemAddon.update.enabled": False,
                "extensions.webextensions.background-delayed-startup": False,
                "general.useragent.locale": "en-US",
                "geo.enabled": False,
                "geo.wifi.uri": "",
                "javascript": True,
                "media.peerconnection.enabled": False,
                "network.IDN_show_punycode": True,
                "network.cookie.cookieBehavior": 1,
                "network.dns.disablePrefetch": True,
                "network.dns.disablePrefetchFromHTTPS": True,
                "network.http.speculative-parallel-limit": 0,
                "network.http.use-cache": False,
                "network.predictor.enable-prefetch": False,
                "network.prefetch-next": False,
                "network.proxy.socks": "127.0.0.1",
                "network.proxy.socks_port": 9150,
                "network.proxy.socks_remote_dns": True,
                "network.proxy.socks_version": 5,
                "network.proxy.type": 1,
                "network.websocket.enabled": False,
                "permissions.default.geo": 2,
                "permissions.default.image": 2,
                "places.history.enabled": False,
                "plugin.scan.plid.all": False,
                "plugin.state.flash": 0,
                "port": 4444,
                "privacy.antitracking.testing": True,
                "privacy.clearOnShutdown.history": True,
                "privacy.clearOnShutdown.offlineApps": True,
                "privacy.clearOnShutdown.openWindows": True,
                "privacy.clearOnShutdown.siteSettings": True,
                "privacy.cpd.cache": False,
                "privacy.cpd.cookies": False,
                "privacy.cpd.history": False,
                "privacy.donottrackheader.enabled": True,
                "privacy.firstparty.isolate": True,
                "privacy.partition.network_state.connection_with_proxy": True,
                "privacy.purge_trackers.enabled": True,
                "privacy.resistFingerprinting": True,
                "privacy.sanitize.sanitizeOnShutdown": True,
                "privacy.spoof_english": 1,
                "privacy.trackingprotection.enabled": True,
                "privacy.trackingprotection.lower_network_priority": True,
                "remoteServerAddr": "localhost",
                "services.sync.engine.history": False,
                "services.sync.prefs.sync.browser.startup.homepage": False,
                "toolkit.legacyUserProfileCustomizations.stylesheets": True,
                "xpinstall.signatures.required": False,
            }
        )




















# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:09:59 2021

@author: Tim
"""

        # ------------------------------------------------------------------ #
        #         Case 2: start or end year not within the timeframe         #
        # ------------------------------------------------------------------ #

        # Case 2 applies if either `year_from` is bigger than `cent_start` or
        # `year_to` is smaller than `cent_end`. In the first case `year_from`
        # needs to be subtracted by 1 and in the second case `year_to` needs
        # to be added 1.

        if (
            len(
                scrape_hist_sub := (
                    scrape_hist.groupby(["country", "state", "municipality"])
                    .agg({"year_from": "min", "year_to": "max"})
                    .reset_index()
                    .query(
                        f"year_from > {self.cent_start} | year_to < {self.cent_end}"
                    )
                    .reset_index(drop=True)
                )
            )
            >= 1
        ):
            print_method(
                "set_query_parameters",
                "Case 2 applied! (year_from or year_to not maxed out)",
            )

            if scrape_hist_sub.loc[0, "year_from"] > self.cent_start:
                year_from = scrape_hist_sub.loc[0, "year_from"] - 1

            elif scrape_hist_sub.loc[0, "year_to"] < self.cent_end:
                year_from = scrape_hist_sub.loc[0, "year_to"] + 1
            else:
                raise ValueError

            # The event places like country, state and municipality are the
            # same for both cases.

            (
                self.event_country,
                self.event_state,
                self.event_munic,
            ) = scrape_hist_sub.loc[0, ["country", "state", "municipality"]]

            self.year_to, self.year_from = int(year_from), int(year_from)

            self.page = 1

            return

        # ------------------------------------------------------------------ #
        #      Case 3: Gaps in the timeframe (individual years missing)      #
        # ------------------------------------------------------------------ #

        if (
            len(
                scrape_hist_sub := (
                    scrape_hist.groupby(["country", "state", "municipality"])[
                        ["year_from"]
                    ]
                    .diff()
                    .query("year_from > 1.0")
                )
            )
            >= 1
        ):
            print_method(
                "set_query_parameters",
                "Case 3 applied! (years missing in between / gaps in year series)",
            )

            diff_idx = scrape_hist_sub.index.values[0]
            diff_values = scrape_hist_sub.values[0]

            year_from = (
                scrape_hist.loc[diff_idx, "year_from"] - int(diff_values) + 1
            )

            (
                self.event_country,
                self.event_state,
                self.event_munic,
            ) = scrape_hist.loc[diff_idx, ["country", "state", "municipality"]]

            self.year_to, self.year_from = int(year_from), int(year_from)

            self.page = 1

            return































        # Check whether one of the date columns is empty. NOTE: This is
        # necessary because if one of the date columns should be empty then it
        # will not have the required stata format and thus will
        col_drop_list: List[str] = []
        for col_ in list(convert_dates.keys()):
            if (len(records_df[col_].unique())) == 1:
                col_drop_list.append(col_)
                convert_dates.pop(col_)


        records_df = records_df.drop(columns=col_drop_list, errors="ignore")








records_file = data_dir_user / "records_file.feather"

if not records_file.exists():
    df_records = pd.DataFrame(
        index=range(0),
        columns=["death", "birth", "burial"],
    )
    df_records.reset_index(drop=True, inplace=True)  # type: ignore
    df_records.to_feather(records_file.as_posix())










def replace_partial_str(
        self, str_webelement: WebElement, str_value: str
    ) -> None:
        """Replace partial string in webelements."""
        # Creating dataframe of mismatches

        orig_str = str_webelement.get_property("value")
        str_len = len(orig_str)
        # Create Dataframe holding the value mismatches
        m_df = pd.DataFrame(columns=["str_pos", "str_value"])

        for idx, (i, j) in enumerate(zip(orig_str, str_value)):
            # Get str_pos counting backwards
            pos_ = (
                str_len - idx
            ) - 1  # because the backspace consumes one pos
            # Determine whether the current element of the new and old string match
            match_ = i == j
            if not match_:
                m_df.loc[len(m_df) + 1] = {"str_pos": pos_, "str_value": j}
        # Reset the index because otherwise it does not start from 0
        m_df.reset_index(drop=True, inplace=True)
        # Reverse index order to start with the last element and not the first
        idx2 = sorted(m_df.index, reverse=True)
        # Replace old index through the new reversed one
        m_df = m_df.loc[idx2, :]
        # It is necessary to reset the index again because otherwise reversing it
        # would have had no effect
        m_df.reset_index(drop=True, inplace=True)

        # Replacing mismatches

        action_ = ActionChains(self)
        # Setup code
        action_.move_to_element(str_webelement).pause(0.5).click(
            str_webelement
        ).pause(0.5).send_keys(Keys.END).pause(0.5)
        # Replacement code
        cur_pos = 0
        for pos_, val_ in m_df.itertuples(index=False):

            while cur_pos < pos_:
                action_.send_keys(Keys.ARROW_LEFT).pause(0.5)
                cur_pos += 1
            action_.send_keys(Keys.BACKSPACE).pause(0.5).send_keys(val_).pause(
                0.5
            )

        action_.perform()


# Future Implementations
from __future__ import annotations
    def check_page_loaded_old(self) -> None:
        """Wait for the page to be loaded."""
        print_method(
            "check_page_loaded", "I'm waiting for the page to load..."
        )
        while True:
            # Make sure page has properly loaded by trying to get the number
            # of found records.
            results = self.get_filter_results()
            if results > 0:
                print_method_success("check_page_loaded", "page loaded!")
                break
            sleep(1)
def not_none(iterable: Iterable[Any]) -> bool:
    """Test if all elements are not None."""
    for element in iterable:
        if element is None:
            return False
    return True
def wait_for_url_change_old(self, current_url: str) -> None:
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
    circle_count = 0
    print_method(
        "wait_for_url_change", "I'm waiting for the URL to change..."
    )
    while True:
        new_url = furl(self.driver.current_url).pathstr
        if circle_count > 15:
            raise TimeoutError(
                "wait_for_url_change: The url change took too long!."
            )
        if new_url != current_url:
            print_method_success("wait_for_url_change", "url changed!")
            break

        sleep(1)
        circle_count += 1
def by_resolver(
    by_value: Literal["class", "css", "id", "name", "xpath"]
) -> str:
    """Return the locator name as expected by selenium.

    Parameters
    ----------
    by_value : {"class", "css", "id", "name", "xpath"}
        Name of selector to use.

    Returns
    -------
    str
        Name of valid selenium selector.
    """
    by_resolve = {
        "class": By.CLASS_NAME,
        "css": By.CSS_SELECTOR,
        "id": By.ID,
        "name": By.NAME,
        "xpath": By.XPATH,
    }
    return by_resolve.get(by_value, "Invalid day of week")


class FirefoxBrowser(Firefox):
    """Start Firefox with modified settings."""

    def __init__(
        self,
    ) -> None:
        options = FirefoxOptions()
        options.headless = False
        options.accept_insecure_certs = True

        super().__init__(
            options=options,
            executable_path=FilePaths.geckodriver_path.as_posix(),
            service_log_path=devnull,
        )

    def find_by_css(self, css_value: str) -> WebElement:
        """Find webelement by css selector."""
        return self.find_element(by=By.CSS_SELECTOR, value=css_value)

    def find_all_by_css(self, css_value: str) -> List[WebElement]:
        """Find all webelement by css selector."""
        return self.find_elements(by=By.CSS_SELECTOR, value=css_value)

    def close_browser(self):
        """Close browser instance."""
        self.delete_all_cookies()
        self.close()

    def wait_for_element_presence(
        self, css_value: str, timeout_secs: int = 90
    ) -> WebElement:
        """Wait for the presence of the element to be located."""
        return WebDriverWait(self, timeout_secs).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_value))
        )

    def wait_for_element_clickable(
        self, css_value: str, timeout_secs: int = 90
    ) -> WebElement:
        """Wait for the presence of the element to be located."""
        return WebDriverWait(self, timeout_secs).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_value))
        )

    def find_button(self, css_selector: str) -> WebElement:
        """Find button using css selector and click it."""
        button_field = self.wait_for_element_presence(css_selector)

        button_field.click()

        return button_field


try:
    # Check if the username was already taken and use the
    # the suggested username
    name_sugg_field = self.driver.find_element_by_css_selector(
        'span[ng-click="chooseUsername(usernameSuggestions[0])"]'
    )
    # Click to select the suggested username
    name_sugg_field.click()
    sleep(1)
    # Get the element of the username field
    username_field = self.driver.find_element_by_css_selector("#username")
    # Retrieve new username proposed by familysearch and replace
    # the old username by the new one
    self.user_account_name = username_field.get_property("value")
except NoSuchElementException:
    pass


def get_current_page_number(self, peek: bool = False) -> int:
    """Get current page as integer."""
    # Make sure methods is only called when on the records page
    try:
        cur_page = int(
            furl(self.driver.current_url).query.params[
                "offset"
            ]  # type: ignore
        )
    except KeyError:
        # Key error is usually raised when the key "offset" cannot be
        # found which is usually a consequence of the url not having that
        # parameter which in turns usually means that the current page
        # is page 1 (displayed in the url then as page 0).
        cur_page = 0

    # The page obtained through the url needs to be increased by 1 to
    # obtain the same page number as it is displayed at the buttom of
    # each records page.
    cur_page = cur_page // 100 + 1
    if not peek:
        self.page = cur_page
        print(f"get_current_page_number: Setting current page to {self.page}")

    return cur_page


def get_results_count_into_limit(self, country: str) -> None:
    """
    Get the right timeframe to get approximately 50000 results.

    Parameters
    ----------
    fallback_year : int, optional
        Year to start from if a history cannot be found.
        The default is 1700.

    Returns
    -------
    None.

    """
    self.set_query_years(country)

    while True:

        self.start_search_query(close_bar=False)

        results_count = self.get_filter_results()

        if results_count >= 5000:

            if results_count < 7000:
                # If the results count is not above 70000 then the overhead,
                # meaning the results for this range that would be "lost"
                # is still acceptable.
                print("estimate reached!")
                self.save_scrape_history()
                return
            elif self.last_year < (self.year_to - 1):
                # Otherwise, meaning if the results are about 70000 then we
                # should try going back in order to bring the results overhead
                # within an acceptable range.
                self.year_to -= 1
                continue
            else:
                print("estimate reached!")
                self.save_scrape_history()
                return

        self.last_year = self.year_to

        # If the year has reached a certain level then the year increment
        # should be set to 1.

        if self.year_to >= 1700:
            if results_count < 1000:
                self.year_to += 30
            elif results_count < 2000:
                self.year_to += 20
            else:
                self.year_to += 10
        elif self.year_to >= 1800:
            self.year_to += 5
        elif self.year_to >= 1900:
            self.year_to += 1
            continue

        sleep(5)


def start_scraping(self):
    """Initialize the webscraping of familysearch."""
    self.load_scrape_history()
    self.set_preferences_to_all_information()
    self.start_search_query()
    self.set_page_size()

    if self.get_current_page_number(peek=True) != self.page:
        self.scroll_down_page()
        self.move_to_page(self.page)

    while self.page < 49:
        self.scrape_elements()
        self.udpate_scrape_history_page()

        self.scroll_down_page()
        self.next_page()
        sleep(5)


@cache
def load_municipalities(self, country: str) -> pd.DataFrame:
    """Load municipality dataframe and cache it for later use."""
    # Make sure that the supplied country is always in lower case
    country = country.lower()

    # Set datapath pointing to the current file of interest
    data_path = FilePaths.munic_path.joinpath(
        f"{country}_municipalities.feather"
    )

    # Load municipalities for the scraping.
    df_mu = pd.read_feather(data_path)

    # Rename the municipality column
    df_mu.rename(columns={"Name": "municipality"}, inplace=True)

    # Insert new column for the state of the municipalities
    df_mu.insert(1, "state", [np.nan] * len(df_mu), True)

    # Set the value of the new column equal to the municpalities column if the
    # "Status" column indicates that it's a state.
    df_mu.loc[df_mu["Status"] == "State", "state"] = df_mu.loc[
        df_mu["Status"] == "State", "municipality"
    ]

    # Replace all empty values with the last non empty value.
    df_mu.ffill(inplace=True)

    # Drop all rows that contain states
    df_mu = df_mu[df_mu["Status"] != "State"]

    df_mu = df_mu[["municipality", "state"]]

    df_mu.reset_index(drop=True, inplace=True)

    df_mu.sort_values(
        ["state", "municipality"],
        inplace=True,
        na_position="last",
        ignore_index=True,
    )

    df_mu["municipality"] = [
        self.pat_arrow_brac.search(mun_).group(0)
        if self.pat_arrow_brac.search(mun_) is not None
        else mun_
        for mun_ in df_mu["municipality"]
    ]

    df_mu["municipality"] = [
        self.pat_no_brac.search(mun_).group(0).strip()
        if self.pat_no_brac.search(mun_) is not None
        else mun_
        for mun_ in df_mu["municipality"]
    ]

    return df_mu

    def get_filter_results(self) -> int:
        """Get number of found records."""
        while True:
            try:
                self.botcheck_test()
                self.survey_popup()
                filter_results = self.driver.find_element_by_css_selector(
                    "#resultsContainer > div > div:nth-child(1) > div > div > h5 > div > h5"
                ).text

                filter_br = self._pat_br_int.search(filter_results).group(0)

                filter_int = int(self._pat_sub_dec.sub("", filter_br))

                break
            except NoSuchElementException:
                sleep(1.5)

        return filter_int


def set_query_places(self, country: str) -> Tuple[str, str, str]:
    """Set event_munic, event_state and event_country for the query."""
    # Load dataframe containing the municipalities.
    munic_df = self.load_municipalities(country)

    # Load scraping history, after that group the dataframe and only keep rows
    # that have the max value of the variable "year_to", reset the index after
    # to obtain the for the coming merge necessary variable "state" and
    # "municipality" and drop the column "country" as it is not existent in
    # the municipality dataframe.
    #
    # NOTE: the following computation is valid even if the scrape history
    # dataframe is empty!
    scrape_history = (
        pd.read_feather(FilePaths.history_file)
        .groupby(["country", "state", "municipality"])["year_to"]
        .max()
        .reset_index()
    )

    # Based on the scrape history: remove all rows for which a scrape history
    # was found with a "year_to" value greater than 1900.
    munic_df_sub = (
        munic_df.merge(
            scrape_history, how="left", on=["country", "state", "municipality"]
        )
        .query("year_to < 1900 | year_to.isnull()", engine="python")
        .drop(columns="year_to")
    )

    country, state, municipality = munic_df_sub.iloc[0]

    self.event_munic = municipality

    self.event_state = state

    self.event_country = country.title()

    return municipality, state, country


def set_query_years(self, country: str) -> None:
    """Set year_from and year_to for the query."""
    fallback_year = 1700

    self.set_query_places(country)

    df_hist = pd.read_feather(FilePaths.history_file)

    correct_columns = df_hist.columns == [
        "country",
        "state",
        "municipality",
        "year_from",
        "year_to",
        "results_count",
        "page",
        "page_max",
        "created_at",
    ]

    assert (
        correct_columns.all()
    ), "_get_query_years: history_file has not the right format!"

    assert isinstance(
        self.event_country, str
    ), "_get_query_years: event_country is not set!"
    assert isinstance(
        self.event_state, str
    ), "_get_query_years: event_state is not set!"
    assert isinstance(
        self.event_munic, str
    ), "_get_query_years: event_munic is not set!"

    hist_sub = df_hist.query(
        "&".join(
            [
                f"country == '{self.event_country}'",
                f"state == '{self.event_state}'",
                f"municipality == '{self.event_munic}'",
            ]
        )
    )["year_to"]

    year_to = hist_sub.max() if len(hist_sub) >= 1 else fallback_year

    self.year_from = int(year_to) + 1

    self.year_to = int(year_to) + 1

    msg_ = f"""
    year_from: {self.year_from}, year_to: {self.year_to},
    event_munic: {self.event_munic}, event_state: {self.event_state},
    event_country: {self.event_country}
    """

    msg_ = " ".join(msg_.split())

    # print(msg_)


def load_scrape_history(self) -> pd.Series:
    """
    Get range of familysearch sites to scrape.

    Raises
    ------
    ValueError
        If no history is present.

    Returns
    -------
    hist_return : pd.Series
        Parameters for the scrape.

    """
    hist_df = pd.read_feather(FilePaths.history_file)

    hist_range = hist_df.query("page < 48")

    if len(hist_range) == 0:
        raise ValueError("No scrape history present!")

    hist_return = hist_range.iloc[0]

    self.event_country = str(hist_return.country)
    self.event_state = str(hist_return.state)
    self.event_munic = str(hist_return.municipality)
    self.year_from = int(hist_return.year_from)
    self.year_to = int(hist_return.year_to)
    self.page = int(hist_return.page) + 1

    return hist_return
