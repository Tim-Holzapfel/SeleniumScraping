# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 00:26:19 2021

@author: Tim
"""


# while True:
#     hist_df.get_results_count_into_limit("mexico")

# -------------------------------------------------------------------------- #
#                            Records scraping part                           #
# -------------------------------------------------------------------------- #
# while True:
#     records_df.start_scraping()


#  scraped_data = load_scraped_data()

country = "Mexico"
munic_df = hist_df.load_municipalities(country)

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


hist_df.test_for_no_results_found()


t1 = driver.find_element_by_css_selector(":root")

t1.send_keys(list(Keys.PAGE_UP))

for i in len(admin_df):
    # Set preference in "advanced search" to "all information"
    nav_fs.set_preferences_to_all_information()

    # Retrieve and set the query arguments necessary for the familysearch query
    hist_df.set_query_parameters(country)

    # Summon the more options side page and enter the previously set query
    # arguments
    hist_df.start_search_query()

    # Retrieve the number of found records and append it together with
    # municipality, state, country, year_from and year_to to the scrape history
    # index
    scrape_history = hist_df.save_scrape_history()

    if hist_df.test_for_no_results_found():
        print("No results found for current qurey, continuing!")
        continue

    # If the current page is not also the last page of the current query then
    # scrape all pages until we have reached the last page
    while records_df.page != records_df.page_max:
        # Scrape the records displayed on the current page
        scraped_records = records_df.scrape_elements()

        # Replace the page number of the scrape history for the current municipality
        # with the current page number to mark the current page in the
        # scrape history record as finished
        hist_df.udpate_scrape_history_page()

        # Scroll down to the page end
        nav_fs.scroll_down_page()

        # Navigate to the next page
        nav_fs.next_page()
        sleep(5)

    # If the current page should also be the last page of the current query
    # then we only need to scrape the page and update the scrape history
    # without the other two steps

    # Scrape the records displayed on the current page
    scraped_records = records_df.scrape_elements()

    # Update scrape history
    records_df.udpate_scrape_history_page()


nav_fs.event_place.split(", ")

scraped_data = nav_fs.load_scraped_data()

hist_df.year_from = None


country, munic = mexico_mu.split(", ")

mexico_mu


nav_fs.botcheck_test()


records_df.page_test()

records_df.set_page_to_current_page()

records_df.year_from


nav_fs.page_test()
nav_fs.set_page_to_current_page()


initial_results_ = nav_fs.get_filter_results()


dir(nav_fs)
dir(hist_data)
hist_data.year_from

nav_fs._year_to += 10

nav_fs.sidebar_more_options_selection()
increment_results = nav_fs.get_filter_results()


inc_increase = increment_results - initial_results_

increment_results + inc_increase


nav_fs._event_place = mexico_mu
nav_fs._year_from = 1800
nav_fs._year_to = 1830
nav_fs.sidebar_more_options_selection()


records_df = RecordsData(driver)


records_df.scrape_elements()

nav_fs.scroll_down_page()

nav_fs.next_page()


page_tab = driver.find_element_by_name("per-page")

dir(page_tab)

page_tab.text


page_tab.get_property("value")


import time
from progressbar import ProgressBar

with ProgressBar(max_value=10) as bar:
    for i in range(10):
        time.sleep(0.1)
        bar.update(i)


nav_fs.page


abs(results_ - 50000)


nav_fs._year_from += 10

nav_fs.sidebar_more_options_selection()


nav_fs._botcheck_test()


dir(driver)


"q_deathLikeDate_to"
death_year_from_to = driver.find_element_by_name("q_deathLikeDate_to")

death_year_from_to = driver.find_element_by_css_selector(
    "input[name*='q_deathLikeDate_to']"
)


dir(death_year_from_to)
death_year_from_to.tag_name
death_year_from_to.text

death_year_from_to.get_property("value")
death_year_from_to.get_attribute("value")

nav_fs.check_page_loaded()


close_button = driver.find_element_by_css_selector(
    "button[aria-label='Close']"
)

close_button.clear()


action_ = ActionChains(driver)

dir(action_)

from selenium.webdriver.common.utils import Keys

results_error.text


action_.pause(2)


field_string = "1930"

input_delay = wait_dist(len(field_string))

death_year_from_to = driver.find_element_by_name("q_deathLikeDate_from")


action_ = ActionChains(driver)

action_.move_to_element(death_year_from_to)

action_.double_click(death_year_from_to).pause(1)

action_.send_keys(list(Keys.DELETE))

action_.perform()


Keys.DELETE

action_ = (
    ActionChains(driver)
    .move_to_element(death_year_from_to)
    .click(death_year_from_to)
    .pause(1)
)

for idx, i in enumerate(field_string):
    action_.pause(input_delay[idx])
    action_.send_keys(list(i))

action_.perform()


from time import sleep


remove_event_buttons = driver.find_elements_by_css_selector(
    "button[aria-label^='Remove' i]:not([aria-label*='Death' i])"
)

for button_ in remove_event_buttons:
    button_.click()
    sleep(1)


remove_event_button.text

t1 = remove_event_button[0]

t2 = remove_event_button[1]

t2.text

death_button = driver.find_element_by_name("Death-chip")

dir(death_button)
death_button.is_enabled()


len(remove_event_button)


pat_auth = re.compile(r"cis-web\/oauth")

fs_url = driver.current_url


pat_auth.search(fs_url)


driver.find_element_by_id("errorAuthentication")


info_sheet = driver.find_element_by_css_selector("div.css-1r9bn5-infoSheetCss")

info_sheet = driver.find_element_by_css_selector("div[class*='infoSheet']")


dir(info_sheet)


info_sheet.is_displayed()


dir(driver)


nav_fs.next_page()
nav_fs.scroll_down_page()


records_df = RecordsData(driver)

records_df.scrape_elements()

hist_df = records_df.load_scraped_data()

#


"#resultsContainer > div > div.non-mobile.css-2glp8-containerCss > span.css-1wiv1cj-thinganatorCss > button:nth-child(5)"


def next_page(self):

    next_page_button = self.driver.find_element_by_css_selector(
        'button[aria-label*="Go to next Page. Currently on Page"]'
    )

    next_page_button.click()


"Go to next Page. Currently on Page 1 of 245"


t2 = pat_sub_dec.sub("", "298,212,048")


dir(t2)


t2.format()

t1 = pat_bra_int.search("(?<=\().*(?=\))", filter_results.text).group(0)
t2 = re.sub(",", "", t1)
t3 = int(t2)


df_records: pd.DataFrame = pd.read_feather(FilePaths.records_file)

val_pat = re.compile(
    r"(?<=Birth|Death|Burial|Father\:|Mother\:|Spouse\:).*", flags=re.S
)
key_pat = re.compile(r"(Birth|Death|Burial|Father|Mother|Spouse)", flags=re.S)


table_body = driver.find_element_by_css_selector(
    "#resultsContainer > div > div:nth-child(2) > table > tbody"
)

table_cells = table_body.find_elements_by_css_selector("tr")
# %% Loop part


date_pat = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November)?\s?\d{4}$"
)


def not_none(iterable: Iterable[str]) -> bool:
    """Test if all elements are not None."""
    for element in iterable:
        if not bool(element):
            return False
    return True


d = defaultdict(dict)

i = len(df_records) + 1

for t_cell in table_cells:

    # Name for the dictionary that is created for the current records entry
    d_name = f"{i:03}"

    full_name = t_cell.find_element_by_css_selector("div.css-10mjg2w-titleCss")

    d[d_name]["name"] = full_name.text

    role_entry = t_cell.find_elements_by_css_selector("div.css-1rgta3")

    for idx, t_str in enumerate(role_entry):

        if idx == 0:
            role_collection_str = t_str.text.split("\n")

            if len(role_collection_str) == 2:
                role_ = role_collection_str[0]
                collection_ = role_collection_str[1]

                d[d_name]["role_respondant"] = role_
                d[d_name]["name_collection"] = collection_
        else:
            key_ = key_pat.search(t_str.text)
            value_ = val_pat.search(t_str.text)

            # Only continue if key_ and value_ are existent because both
            # key_.group(0) and value_.group(0) will raise an error otherwise.
            if not_none([key_, value_]):
                value_ = value_.group(0)
                key_ = key_.group(0).lower()

                # "death", "birth", "burial" contain information about either
                # the date of the respective event or the location or both. The
                # string starts with the date if both date and location are
                # given followed by carriage return (\n) and the location.
                if key_ in ["death", "birth", "burial"]:
                    value_ = value_.split("\n")

                    if len(value_) == 2:
                        key_date = f"{key_}_date"
                        d[d_name][key_date] = value_[0]
                        value_ = value_[1]
                        key_ = f"{key_}_location"
                    elif date_pat.search(value_[0]):
                        # It is necessary to determine whether the string
                        # information about the date or the location if no
                        # carriage return (\n) is present.
                        key_ = f"{key_}_date"
                        value_ = value_[0]
                    else:
                        key_ = f"{key_}_location"
                        value_ = value_[0]

                d[d_name][key_] = value_

    i += 1

df_records_ext = pd.DataFrame.from_dict(
    d,
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


FileExistsError()


int("001")


# %% Test area


t1.astype(int)
dir(t1)

int(t1)


df_test = df_records_ext.reset_index()

dir(df_records_ext)

df_sub.columns

value_1 = None

all([key_, value_1])


parts = ")"

for i in range(1, 12):
    parts += month_name[i] + "|"

parts += "("

parts += [month_name[i] for i in range(1, 12)]


date_str = "April 1708"


dir(date_pat)

date_pat.search(date_str)


t_cell = table_cells[0]

role_entry = t_cell.find_elements_by_css_selector("div.css-1rgta3")

t_str = role_entry[0]

role_collection_str = t_str.text.split("\n")

len(role_collection_str)

role_, collection_


file = "20 April 1699"

datetime.date.isoformat(datetime.datetime.strptime(file, r"%d %B %Y"))


dmy_pat = re.compile(r"^\d{1,2}\s[A-Z][a-z]+\s\d{4}$")
my_pat = re.compile(r"^[A-Z][a-z]+\s\d{4}$")
y_pat = re.compile(r"^\d{4}$")


def form_date(date_str: str, date_format: str):
    return datetime.date.isoformat(
        datetime.datetime.strptime(date_str, date_format)
    )


death_date = [
    form_date(file, r"%d %B %Y")
    if dmy_pat.search(str(file)) is not None
    else form_date(file, r"%B %Y")
    if my_pat.search(str(file)) is not None
    else form_date(file, r"%Y")
    if y_pat.search(str(file)) is not None
    else None
    for file in df_sub["death_date"]
]

death_date = [
    form_date(file, r"%d %B %Y")
    for file in df_sub["death_date"]
    if dmy_pat.search(file) is not None
]


for file in df_sub["death_date"].values:
    dmy_pat.search(file)

t_str = role_entry[2].text


tt = "29 October 1718\nParroquia De Patzcuaro".lower()


t3 = tt.split("\n")
len(t3)

t3[1]

t_cell = table_cells[0]

role_entry = t_cell.find_elements_by_css_selector("div.css-1rgta3")

t_str = role_entry[0].text


dir(val_pat.search(t2))


role_entry[1].text

filter_results = driver.find_element_by_css_selector(
    "#resultsContainer > div > div:nth-child(1) > div > div > h5 > div > h5"
)


t1 = re.search("(?<=\().*(?=\))", filter_results.text).group(0)
t2 = re.sub(",", "", t1)
t3 = int(t2)


t3 / 100


dir(t1)
float(t1)

t1.group(0)


nav_fs.sidebar_more_options_selection()

hist_df = HistoryData()

dir(hist_df)


hist_df.event_place

# Summon more options menu
more_options_button = driver.find_element_by_css_selector(
    "div > button:nth-child(2)"
)
more_options_button.click()

# Remove the "Any" selection
remove_event_button = driver.find_element_by_css_selector(
    "button[aria-label='Remove Event']"
)
remove_event_button.click()

# Click on the "death" button
death_button = driver.find_element_by_name("Death-chip")
death_button.click()

# Death place formfield
death_place_field = driver.formfield_enter("#deathLikePlace", "Mexico")


def enter_death_year(css_selector: str, year_str: str) -> None:

    death_year_from_to = driver.find_element_by_name(css_selector)

    ActionChains(driver).move_to_element(death_year_from_to).click(
        death_year_from_to
    ).send_keys(year_str).perform()

    return


enter_death_year("q_deathLikeDate_from", "1920")

enter_death_year("q_deathLikeDate_to", "1920")


search_button = driver.find_element_by_css_selector(
    "div.css-nzy20i-bleedCss > div > div > button:nth-child(1)"
)

search_button.click()


driver.formfield_enter("q_deathLikeDate_from", "1900", "name")


death_place_field.text
death_place_field = driver.find_element_by_css_selector("#deathLikePlace")


death_place_field.send_keys(list("1900"))


t1 = driver.formfield_enter('//*[@id="anyPlace"]', "Mexico", "xpath")


search_button = driver.find_button(
    '//*[@id="search-form"]/div/div[5]/div/button[1]', "xpath"
)


t1.click()

type(fs_group)
dir(fs_group)


next(t1)


if __name__ == "__main__":
    driver = TorBrowser(
        event_type="death",
        event_place="Brazil",
        year_from=1000,
        year_to=1900,
        headless=False,
    )

    msg_iter = Messages()

    driver.set_window_position(**{"x": -1914, "y": 19})

    acpr = ActiveProfiles()

    profile_iter = acpr.profile_iter()

    msg_iter = Messages()

    current_profile = next(profile_iter)

    driver.delete_all_cookies()
    # Go to familysearch.org website
    driver.get("https://www.familysearch.org/en/")

    time.sleep(2)

    # %% Login to Website
    website_login(driver, current_profile)

    # %% Navigating sub menus
    navigate_sub_menus(driver)

    # %% Select event
    event_selection(driver=driver)

    # %% Load scraping history
    # driver.load_history()

    driver.get_number_of_results()

    driver.page = 3
    if driver.page > 1:
        data_page_size(driver)
        next_page_click(driver)
    while True:
        botcheck_test(driver, msg_iter)
        # Download xls file with records.
        scrape_elements(driver)
        # Increment the page number by one.
        driver.save_history()
        # Click on the next page button.
        next_page_click(driver)
