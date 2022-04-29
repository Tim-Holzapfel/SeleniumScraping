



    def survey_popup(self):
        """Decline the survey popup if it should appear."""
        self.driver.wait_for_element_clickable(
            "button[class*='QSIWebResponsiveDialog']:nth-child(2)"
        )



logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=FilePaths.user_error_log,
    filemode="a",
)

self.logger = logging.getLogger("error_log")





def check_page_loaded(self, next_page: int) -> None:
    """Test if the page has been fully loaded.

    Parameters
    ----------
    driver : TorBrowser
    Webdriver initiated by `TorBrowser`..

    Raises
    ------
    TypeError
        If the function is applied on a webpage other than the
        Familysearch search webpage.

    Returns
    -------
    None
    """
    # %% Context test
    f = furl(self.driver.current_url)

    search_page_check = f.pathstr == "/search/record/results"

    if not search_page_check:
        raise WrongPage(
            """A 'page-loaded' test can only be performed
            while on the results page."""
        )
    # %% Main function
    while True:

        self.detect_iframe()

        node1 = self.driver.wait_for_element(
            ".full-width > SEARCH-ARTIFACT-RESULTS"
        )

        # First Shadow Root
        shadow_root1 = expand_se(self.driver, node1)[2]

        # Second Node
        node2 = shadow_root1.find_element_by_css_selector("sr-panels")

        # Second Shadow Root
        shadow_root2 = expand_se(self.driver, node2)[1]

        # Third Node
        node3 = shadow_root2.find_element_by_css_selector(
            "sr-records.query-source"
        )

        display_results = expand_se(self.driver, node3)[3]

        try:
            end_str = findall(
                r"(?<=\-)(\d+)(?:[.,]?)(\d*)", display_results.text
            )[0]
        except IndexError as bce:
            raise BotCheckInvoked("No page information displayed.") from bce

        end_int = int("".join(end_str))

        active_page = end_int // 100

        # TODO: change the error into a warning and rewrite the
        # code in a manner that the last page is scraped and the
        # code stops with exit 0.

        if end_int % 100 != 0:
            raise LastPageError("Last page of query reached.")

        sleep(5)

        if active_page == next_page:
            break


def botcheck_test(self, msg_iter: Optional[Messages] = None) -> None:
    """Test for the presence of botchecks.

    Parameters
    ----------
    driver : TorBrowser
        Webdriver initiated by `TorBrowser`.
    msg_iter : Iterable[str]
        Container for user messages.

    Returns
    -------
    None
    """
    self.click_consent_button()

    node_1 = self.driver.wait_for_element(
        '//*[@id="main-content-section"]/div[6]/search-artifact-results',
        "xpath",
    )

    # 'search-artifact-results'
    # node_1.tag_name

    node_1_sroot = expand_se(self.driver, node_1)[2]

    # %% Bot alert test
    # Test for the presence of a bot alert

    retry_count = 1
    if msg_iter is not None:
        print(msg_iter.botcheck_test)
    while True:
        if retry_count == 1:
            try:
                node_1_sroot.find_element_by_css_selector("div[role='alert']")
                retry_count += 1
                if msg_iter is not None:
                    print_red(msg_iter.botcheck_detected_first)
                self.driver.refresh()
                sleep(15)
            except NoSuchElementException:
                if msg_iter is not None:
                    print_green(msg_iter.no_botcheck_first)
                # No alert found, continuing
                break
        elif retry_count == 2:
            try:

                node_1 = self.driver.wait_for_element(
                    '//*[@id="main-content-section"]/div[6]/search-artifact-results',
                    "xpath",
                )

                node_1_sroot = expand_se(self.driver, node_1)[2]
                node_1_sroot.find_element_by_css_selector("div[role='alert']")
                if msg_iter is not None:
                    print_red(msg_iter.botcheck_detected_second)
                self.driver.refresh()
                retry_count += 1
                sleep(15)
            except NoSuchElementException:
                # No alert found, continuing
                if msg_iter is not None:
                    print_green(msg_iter.no_botcheck_second)
                break
        elif retry_count == 3:
            try:

                node_1 = self.driver.wait_for_element(
                    '//*[@id="main-content-section"]/div[6]/search-artifact-results',
                    "xpath",
                )

                node_1_sroot = expand_se(self.driver, node_1)[2]
                if msg_iter is not None:
                    print_red(msg_iter.botcheck_detected_final)
                raise BotCheckInvoked("Familysearch invoked a botcheck!.")
            except NoSuchElementException:
                # No alert found, continuing
                if msg_iter is not None:
                    print_green(msg_iter.no_botcheck_final)
                break


def event_selection_old(self) -> None:
    """Select event for the records search."""
    self.click_consent_button()

    # fs-search-form node
    fs_search_form = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fs-search-form"))
    )

    fs_root = expand_se(self.driver, fs_search_form)[2]

    # fs-search-field-group
    fs_group = fs_root.find_element_by_css_selector(
        "sf-search-field-group[group-id='event']"
    )

    # Shadow root containing the buttons
    button_root = expand_se(self.driver, fs_group)[1]

    form_buttons = button_root.find_elements_by_css_selector(
        "ul.form-trigger li > legend"
    )

    # Looping through all buttons in order to make sure non is active.
    for button in form_buttons:
        if button.get_attribute("class").endswith("active"):
            button.click()
            sleep(0.5)

    if self.event_type == "birth":
        form_buttons[0].click()
    elif self.event_type == "marriage":
        form_buttons[1].click()
    elif self.event_type == "residence":
        form_buttons[2].click()
    elif self.event_type == "death":
        form_buttons[3].click()
    elif self.event_type == "any":
        form_buttons[4].click()

    sleep(2)

    # %% textfield
    fs_textfield = fs_root.find_element_by_css_selector(
        "sf-search-field[field-type='place']"
    )

    tf_root = expand_se(self.driver, fs_textfield)[1]

    input_field = tf_root.find_element_by_css_selector("input[type='text']")

    ActionChains(self.driver).move_to_element(input_field).click(
        input_field
    ).send_keys(self.event_place).perform()

    # %% year range (Optional)
    # Only continue with the selection of years if at least either the
    # year_from or the year_to argument was explicitly given and not None.
    if self.year_from is not None or self.year_to is not None:
        sleep(1)
        fs_year = fs_root.find_element_by_css_selector(
            "sf-search-field[field-type='year']"
        )

        year_root = expand_se(self.driver, fs_year)[1]

        year_selection = year_root.find_elements_by_css_selector(
            "input[type='text']"
        )

        # If the year_from argument was given.
        if self.year_from is not None:
            sleep(3)
            year_from_field = year_selection[0]

            ActionChains(self.driver).move_to_element(year_from_field).click(
                year_from_field
            ).send_keys(self.year_from).perform()

        # If the year_to argument was given.
        if self.year_to is not None:
            sleep(3)
            year_to_field = year_selection[1]

            ActionChains(self.driver).move_to_element(year_to_field).click(
                year_to_field
            ).send_keys(self.year_to).perform()

    # %% Restrict search by country (optional)

    if self.country is not None:
        sleep(5)
        # fs-search-field-group
        fs_country = fs_root.find_element_by_css_selector(
            "sf-search-field[field-type='location']"
        )

        country_root = expand_se(self.driver, fs_country)[1]

        country_picker = country_root.find_element_by_css_selector(
            "country-picker"
        )

        picker_root = expand_se(self.driver, country_picker)[1]

        birch_typehead = picker_root.find_element_by_css_selector(
            "#recordCountry"
        )

        typehead_root = expand_se(self.driver, birch_typehead)[2]

        country_input_field = typehead_root.find_element_by_css_selector(
            "#input"
        )

        ActionChains(self.driver).move_to_element(country_input_field).click(
            country_input_field
        ).send_keys(self.country).click().perform()

    # %% Submit button
    submit_button = fs_root.find_element_by_css_selector(
        "button[type='submit']"
    )
    submit_button.click()


def set_page_size(self) -> None:
    """Set number of records to show per page."""

    def _get_results_range(_results: str) -> str:
        """Get page range of results."""
        page_range = match(r"^\d{1}\-\d{2,3}(?=\sof)", _results)
        try:
            assert isinstance(page_range, str)
            page_index = page_range[0]
        except AssertionError as excp:
            raise BotCheckInvoked("Could not find pagesize buttons.") from excp

        return page_index

    def _data_page_resuls() -> WebElement:

        self.detect_iframe()

        node1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".full-width > SEARCH-ARTIFACT-RESULTS")
            )
        )

        # First Shadow Root
        shadow_root1 = expand_se(self.driver, node1)[2]

        # Second Node
        node2 = shadow_root1.find_element_by_css_selector("sr-panels")

        # Second Shadow Root
        shadow_root2 = expand_se(self.driver, node2)[1]

        # Third Node
        return shadow_root2.find_element_by_css_selector(
            "sr-records.query-source"
        )

    # First Node

    entry_node = _data_page_resuls()

    display_results_entry = expand_se(self.driver, entry_node)[3]

    # %% Page entering assertion

    # When entering the page it should say "1-20 of ... Results for ..."
    results_entry = _get_results_range(display_results_entry.text)

    # Making sure that that is the case
    pgsz_20_asrt = results_entry == "1-20"

    assert pgsz_20_asrt, "Pagesize is not 20."

    # %% Changing page size

    # Node holding the search results count
    node4 = expand_se(self.driver, entry_node)[4]

    node5 = node4.find_element_by_css_selector("sr-page-size.query-source")

    shadow_root_size = expand_se(self.driver, node5)[1]

    button_size = shadow_root_size.find_element_by_css_selector(
        'button[data-page-size="100"]'
    )

    button_size.click()

    sleep(3)

    # %% Page change assertion

    while True:
        exit_node = _data_page_resuls()

        display_results_exit = expand_se(self.driver, exit_node)[3]

        # After clicking the button it should
        # say "1-100 of ... Results for ..."
        results_exit = _get_results_range(display_results_exit.text)

        # Repeat until the page displays the required text
        if results_exit == "1-100":
            break

        sleep(2)


def next_page_click(self, mult_pgs: Optional[bool] = False):
    """Click on the next page button on the current website."""

    def _get_current_page():
        """Get current webbrowser page."""
        f = furl(self.driver.current_url)

        page_count = int(f.args["count"])
        page_offset = int(f.args["offset"])

        return page_offset // page_count + 1

    def _test_int(int_str: str) -> Union[int, float]:
        """Convert input object to integer or NaN."""
        try:
            return int(int_str)
        except ValueError:
            return np.nan

    while True:
        # If the consent button didn't appear on the first page then it is
        # likely that it will appear later on.

        self.botcheck_test()

        # %% Code to find relevant button
        search_node1 = self.driver.find_element_by_xpath(
            '//*[@id="main-content-section"]/div[6]/search-artifact-results'
        )

        search_shadow_root1 = expand_se(self.driver, search_node1)[2]

        search_node2 = search_shadow_root1.find_element_by_css_selector(
            "sr-panels.query-source.query-target"
        )

        search_shadow_root2 = expand_se(self.driver, search_node2)[1]

        search_node3 = search_shadow_root2.find_element_by_css_selector(
            "sr-pager.query-source.desktop"
        )

        search_shadow_root3 = expand_se(self.driver, search_node3)[1]

        # %% Relevant! button list

        # List with all available buttons (including 'previous' and 'next'
        # buttons)
        button_list = search_shadow_root3.find_elements_by_css_selector(
            "button"
        )

        # Get the button labels and convert them to integers
        b_labels = [_test_int(page.text) for page in button_list]

        # Test if the destination page is among the current buttons
        dest_test = self.driver.page in b_labels

        # If the destination page is not among the available buttons then
        # select the button with the 'biggest' page number.

        try:
            page_index = (
                b_labels.index(self.driver.page)
                if dest_test
                else b_labels.index(np.nanmax(b_labels))
            )
        except ValueError:
            raise BotCheckInvoked(
                "Site loaded without navigation bar / page buttons."
            )

        # Webdriver element of the relevant page button
        next_button = button_list[page_index]

        # Y-Position of the next page button
        next_button_pos = next_button.location["y"]

        current_page = _get_current_page()

        # %% Scroll down to button loop
        p_bar_inner = alive_bar(
            total=next_button_pos,
            manual=True,
            title=f"Page {current_page}|Scrolling to page end",
            theme="classic",
        )

        with p_bar_inner as bar_inner:
            while True:
                self.driver.find_element_by_tag_name("body").send_keys(
                    Keys.PAGE_DOWN
                )
                current_pos: float = self.driver.execute_script(
                    "return window.pageYOffset;"
                )
                if (current_pos + 800) >= next_button_pos:
                    bar_inner(1)
                    break
                prog_perc = current_pos / next_button_pos
                bar_inner(prog_perc)
                sleep(default_rng().lognormal(mean=0.5, sigma=1.0, size=1))

        # The value of the "next_button" seems to automatically change
        # when the page is changed so its value needs to be kept constant
        # someway.
        next_button_freeze = int(next_button.text)

        # 'next_button.text' = page number of the next page

        next_button.click()

        # After 'next_button.click()', 'next_button.text' = page number of
        # current page.

        sleep(5)

        self.check_page_loaded(next_button_freeze)

        if next_button_freeze == self.driver.page:
            break


def scrape_elements(self) -> None:
    """Scrape elements from website."""
    self.set_page_size()

    node_1 = WebDriverWait(self.driver, 50).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="main-content-section"]/div[6]/search-artifact-results',
            )
        )
    )

    # 'search-artifact-results'
    # node_1.tag_name

    node_1_sroot = expand_se(self.driver, node_1)[2]

    node_2 = node_1_sroot.find_element_by_css_selector(
        "sr-panels.query-source.query-target"
    )

    # 'sr-panels'
    # node_2.tag_name

    node_2_sroot = expand_se(self.driver, node_2)[1]

    node_3 = node_2_sroot.find_element_by_css_selector(
        "sr-records.query-source"
    )

    # 'sr-records'
    # node_3.tag_name

    node_3_sroot = expand_se(self.driver, node_3)[5]

    # node_3_sroot.tag_name

    node_4_sroot = expand_se(self.driver, node_3_sroot)[2]

    event_nodes = node_4_sroot.find_elements_by_css_selector("sr-cell-events")

    name_nodes = node_4_sroot.find_elements_by_css_selector("sr-cell-name")

    progress_bar = alive_bar(
        total=len(event_nodes),
        title="Looping through nodes",
        theme="classic",
        bar="classic",
    )

    # %% Looping through nodes

    with progress_bar as bar:
        for event_node, name_node in zip(event_nodes, name_nodes):

            event_events = event_node.get_attribute("events")

            events_ = literal_eval(event_events)

            try:
                dict_birth = events_[0]
            except Exception:
                dict_birth = dict({"date": "", "place": ""})
            try:
                dict_death = events_[1]
            except Exception:
                dict_death = dict({"date": "", "place": ""})
            try:
                dict_burial = events_[2]
            except Exception:
                dict_burial = dict({"date": "", "place": ""})

            df_records.loc[len(df_records)] = {
                "index": len(df_records),
                "full_name": name_node.get_attribute("name"),
                "relationship": name_node.get_attribute("relationship"),
                "collection": name_node.get_attribute("collection-name"),
                "birth_date": dict_birth.get("date"),
                "birth_place": dict_birth.get("place"),
                "death_date": dict_death.get("date"),
                "death_place": dict_death.get("place"),
                "burial_date": dict_burial.get("date"),
                "burial_place": dict_burial.get("place"),
            }
            bar()
            sleep(1)

    df_records.drop_duplicates(inplace=True)  # type: ignore
    df_records.to_feather(FilePaths.records_file)  # type: ignore


def expand_se(driver: Firefox, element_node: WebElement) -> List[WebElement]:
    r"""Expand shadow root element and make 'hidden' nodes accesible.

    Parameters
    ----------
    driver : TorBrowser
        Webdriver initiated by `TorBrowser`.
    element_node : WebElement
        Element containing the shadow root node.

    Returns
    -------
    WebElement.

    """
    shadow_root = driver.execute_script(
        "return arguments[0].shadowRoot.children", element_node
    )

    return shadow_root


def get_number_of_results(self) -> int:
    """Retrieve number of found records of the query."""
    node1 = self.driver.wait_for_element(
        ".full-width > SEARCH-ARTIFACT-RESULTS"
    )

    # First Shadow Root
    shadow_root1 = expand_se(self.driver, node1)[2]

    # Second Node
    node2 = shadow_root1.find_element_by_css_selector("sr-panels")

    # Second Shadow Root
    shadow_root2 = expand_se(self.driver, node2)[1]

    # Third Node
    node3 = shadow_root2.find_element_by_css_selector(
        "sr-records.query-source"
    )

    display_results = expand_se(self.driver, node3)[3]

    results_str: str = re.findall(
        r"of\s(\d+)(?:[.,]?)(\d*)", display_results.text
    )[0]

    new_var: int = int("".join(results_str))
    return new_var
    # self.results_count = new_var


 # Make sure page has loaded
 while True:
     sleep(1)
     try:
         page_dropdown = _find_page_size()

         cur_p_size = page_dropdown.first_selected_option.text

         if cur_p_size == "100":
             break
     except NoSuchElementException:
         pass


# If the following try-statement does not result in an error then this
# country has been scraped before and we can continue where we stopped
# last time.

# =============================================================================
#         try:
#             self.page = int(
#                 self.hist_df.page.where(
#                     self.hist_df.country == self._event_place,
#                     self.hist_df.year_from == self._year_from,
#                     self.hist_df.year_to == self._year_to,
#                 ).max()
#             )
#
#             if self.page > 1:
#                 print(
#                     f"It seems that last time we scraped {self._event_place}",
#                     f"we left off at page {self.page}. I will continue where",
#                     "we left off.",
#                 )
#
#         except ValueError:
#             print(
#                 f"I didn't find a scrape history for {self._event_place}.",
#                 "I will beginn at the first page.",
#             )
#             self.page = 1
#             #super().__init__(driver)
# =============================================================================

def _enter_death_year(self, css_selector: str, year_str: str) -> None:
    """Enter death year into the open side-bar."""
    # Element containing the text string of the formfield and obtaining
    # the current value (property value).
    cur_value_ = self.driver.find_element_by_css_selector(
        f"input[name*='{css_selector}']"
    ).get_property("value")

    # If the value to be entered is already present in the formfield
    # then return
    if cur_value_ == year_str:
        return

    # Element containing the year formfield
    death_year_from_to = self.driver.find_element_by_name(css_selector)

    action_ = ActionChains(self.driver)

    action_.move_to_element(death_year_from_to)

    # Double click to select whole field
    action_.double_click(death_year_from_to).pause(1)

    # Press "delete" button to remove any string possibly present.
    action_.send_keys(list(Keys.DELETE))

    input_delay = wait_dist(len(year_str))

    for idx, i in enumerate(year_str):
        action_.pause(input_delay[idx])
        action_.send_keys(list(i))

    action_.perform()

    sleep(1)

    return











def save_scrape_history(self) -> None:
    """Save history of scraped pages of the current country.

    Returns
    -------
    None.
    """
    assert self.event_country is not None, "Country is not set."

    assert self.event_munic is not None, "Municipality is not set."

    assert self.year_from is not None, "year_from is not set."

    assert self.year_to is not None, "year_to is not set."

    # Write current page number, country and time to the scraping
    # history file.

    page_ = self.get_current_page_number()

    self.hist_df.loc[len(self.hist_df)] = {
        "page": page_,
        "country": self.event_country,
        "municipality": self.event_munic,
        "year_from": self.year_from,
        "year_to": self.year_to,
        "created_at": pd.to_datetime("now"),
    }

    self.hist_df.sort_values(
        ["page", "country", "municipality", "year_from", "year_to"],
        inplace=True,
        na_position="last",
        ignore_index=True,
    )

    self.hist_df.drop_duplicates(
        subset=["page", "country", "municipality", "year_from", "year_to"],
        keep="first",
        inplace=True,
        ignore_index=True,
    )

    self.hist_df.dropna(inplace=True)

    self.hist_df.to_feather(FilePaths.history_file)





def scrape_elements(self):
    """Scrape elements from familysearch.org."""

    def _form_date(date_str: str, date_format: str):
        return datetime.date.isoformat(
            datetime.strptime(date_str, date_format)
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

    self.botcheck_test()

    self.set_page_size()

    df_records: pd.DataFrame = pd.read_feather(FilePaths.records_file)

    table_body = self.driver.find_element_by_css_selector(
        "#resultsContainer > div > div:nth-child(2) > table > tbody"
    )

    table_cells = table_body.find_elements_by_css_selector("tr")

    return_dict = collections.defaultdict(dict)

    i = len(df_records) + 1

    j = 0

    with ProgressBar(max_value=len(table_cells)) as bar_prog:
        for t_cell in table_cells:

            # Name for the dictionary that is created for the current
            # records entry
            d_name = f"{i:03}"

            full_name = t_cell.find_element_by_css_selector(
                "div.css-10mjg2w-titleCss"
            )

            return_dict[d_name]["name"] = full_name.text

            role_entry = t_cell.find_elements_by_css_selector(
                "div.css-1rgta3"
            )

            for idx, t_str in enumerate(role_entry):

                if idx == 0:
                    role_collection_str = t_str.text.split("\n")

                    if len(role_collection_str) == 2:
                        role_ = role_collection_str[0]
                        collection_ = role_collection_str[1]

                        return_dict[d_name]["role_respondant"] = role_
                        return_dict[d_name][
                            "name_collection"
                        ] = collection_

                        continue

                key_ = self._key_pat.search(t_str.text)
                value_ = self._val_pat.search(t_str.text)

                # Only continue if key_ and value_ are existent because
                # both key_.group(0) and value_.group(0) will raise an
                # error otherwise.
                if not_none([key_, value_]):
                    value_ = value_.group(0)
                    key_ = key_.group(0).lower()

                    # "death", "birth", "burial" contain information
                    # about either the date of the respective event or the
                    # location or both. The string starts with the date if
                    # both date and location are given followed by
                    # carriage return (\n) and the location.
                    if key_ in ["death", "birth", "burial"]:
                        value_ = value_.split("\n")

                        if len(value_) == 2:
                            key_date = f"{key_}_date"
                            return_dict[d_name][key_date] = value_[0]
                            value_ = value_[1]
                            key_ = f"{key_}_location"
                        elif self._date_pat.search(value_[0]):
                            # It is necessary to determine whether the
                            # information about the date or the location
                            # if no carriage return (\n) is present.
                            key_ = f"{key_}_date"
                            value_ = value_[0]
                        else:
                            key_ = f"{key_}_location"
                            value_ = value_[0]

                    return_dict[d_name][key_] = value_

            i += 1
            j += 1
            bar_prog.update(j)

    df_records_ext = pd.DataFrame.from_dict(
        return_dict,
        orient="index",
        columns=[
            "name",
            "role_respondant",
            "name_collection",
            "birth_date",
            "birth_location",
            "death_date",
            "death_location",
            "burial_date",
            "burial_location",
            "father",
            "mother",
            "spouse",
        ],
    )

    df_records_ext.reset_index(drop=True, inplace=True)

    df_records = df_records.append(df_records_ext, ignore_index=True)

    df_records.to_feather(FilePaths.records_file)

    print(
        f"I successfully scraped page {self.page} of {self.event_country}!"
    )



    def navigate_to_records(self):
        # Find element containing formfield of the place
        ff_dd = self.driver.wait_for_element_presence("#anyPlace")
        ff_dd.clear()

        # Initialize action chain
        action_ = ActionChains(self.driver)

        # Move focus of chain to the formfield
        action_.move_to_element(ff_dd)

        # Generate array of wait time. For each letter in the supplied string
        # an integer with the wait time in seconds will be generated.
        input_delay = wait_dist(len(input_str))

        action_.click(ff_dd).pause(1)

        for idx, i in enumerate(input_str):
            action_.pause(input_delay[idx])
            action_.send_keys(list(i))

        # Sending values to the formfield will trigger a dropdown list containing
        # autocompletion suggestion based on the supplied values. To select
        # the suggestion on top of the dropdown "Enter" needs to be pressed
        # what happens at the end of the chain.
        action_.send_keys(list(Keys.ENTER)).pause(1)

        # The page change can be initiated by simply presseng enter.
        action_.send_keys(list(Keys.ENTER)).pause(1)

        action_.perform()
