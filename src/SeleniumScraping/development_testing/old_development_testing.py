
hist_df = pd.read_feather(FilePaths.history_file)

hist_idx = hist_df.query(
    "&".join(
        [
            f"country == '{nav_fs.event_country}'",
            f"state == '{nav_fs.event_state}'",
            f"municipality == '{nav_fs.event_munic}'",
            f"year_from == {nav_fs.year_from}",
            f"year_to == {nav_fs.year_to}",
        ]
    )
).index.values[0]

hist_df.loc[hist_idx, "page"] = nav_fs.page


t1 = hist_sub.index


dir(hist_sub)


hist_sub = hist_df.query(
    "&".join(
        [
            f"country == '{self.event_country}'",
            f"state == '{self.event_state}'",
            f"municipality == '{self.event_munic}'",
            f"year_from == '{self.year_from}'",
            f"year_to == '{self.year_to}'",
        ]
    )
)


val_pat = re.compile(
    r"(?<=Birth|Death|Burial|Father\:|Mother\:|Spouse\:).*", flags=re.S
)


hist_df._get_query_years(1700)


hist_df = pd.DataFrame(
    columns=[
        "country",
        "state",
        "municipality",
        "year_from",
        "year_to",
        "results_count",
        "page",
        "created_at",
    ]
)
hist_df.reset_index(drop=True, inplace=True)

hist_df.loc[len(hist_df)] = {
    "country": "Mexico",
    "state": "Aguascalientes",
    "municipality": "Asientos",
    "year_from": 1710,
    "year_to": 1820,
    "results_count": 54720,
    "page": None,
    "created_at": pd.to_datetime("now"),
}


hist_df.to_feather(FilePaths.history_file)


scrape_history = load_scraped_history()

scrape_history = scrape_history.fillna(value=0)

scrape_history.to_feather(FilePaths.history_file)

scrape_history["year_to"]


nav_fs.event_country
nav_fs.event_state
nav_fs.event_munic


nav_fs.year_from


hist_df = pd.DataFrame(
    columns=[
        "country",
        "state",
        "municipality",
        "year_from",
        "year_to",
        "results_count",
        "page",
        "created_at",
    ]
)
hist_df.reset_index(drop=True, inplace=True)

hist_df.loc[len(hist_df)] = {
    "country": "Mexico",
    "state": "Aguascalientes",
    "municipality": "Asientos",
    "year_from": 1500,
    "year_to": 1580,
    "results_count": 50000,
    "page": None,
    "created_at": None,
}

hist_df.loc[len(hist_df)] = {
    "country": "Mexico",
    "state": "Aguascalientes",
    "municipality": "Asientos",
    "year_from": 1500,
    "year_to": 1780,
    "results_count": 50000,
    "page": None,
    "created_at": None,
}


hist_df.loc[len(hist_df)] = {
    "country": "Mexico",
    "state": "Aguascalientes",
    "municipality": "Asientos",
    "year_from": 1500,
    "year_to": 1530,
    "results_count": 50000,
    "page": None,
    "created_at": None,
}


hist_sub = hist_df.query(
    "&".join(
        [
            f"country == '{nav_fs.event_country}'",
            f"state == '{nav_fs.event_state}'",
            f"municipality == '{nav_fs.event_munic}'",
        ]
    )
)["year_to"]


hist_sub.max()


def _set_query_years(self):
    hist_sub = hist_df.query(
        "&".join(
            [
                f"country == '{nav_fs.event_country}'",
                f"state == '{nav_fs.event_state}'",
                f"municipality == '{nav_fs.event_munic}'",
            ]
        )
    )["year_to"]

    year_to = hist_sub.max() if len(hist_sub) >= 1 else 1500

    self.year_from = year_to + 10

    self.year_to = year_to + 10

    return year_to


def get_results_count_into_limit(start_year):

    self._set_query_years()

    while True:

        nav_fs.sidebar_more_options_selection(close_bar=False)

        results_count = nav_fs.get_filter_results()

        if results_count >= 50000:
            print("estimate reached!")
            hist_df.save_meta_data()
            return

        self.year_to += 10

        sleep(5)


get_results_count_into_limit(1800)


# %% Start scraping


driver.find_element_by_css_selector("#deathLikeDate")


year_field = driver.find_element_by_css_selector(
    "input[name*='q_deathLikeDate_to']"
)


year_field.get_property("value")


nav_fs.year_from = 1800
nav_fs.year_to = 1800


nav_fs.sidebar_more_options_selection()


nav_fs.event_munic


query_str = nav_fs.event_country + ", " + nav_fs.event_munic

in_str = "TEst1, Munic1"


str(in_str)


mexico_munic = hist_df.load_municipalities("mexico")


query_str = "Asientos, Aguascalientes, Mexico"

driver.formfield_enter("deathLikePlace", "Test")


ff_deathplace = driver.find_css("#deathLikePlace")


ff_deathplace.get_property("value")


dir(t1)


Select(t1)


t1 = driver.find_element_by_css_selector("#deathLikePlace")

action_ = ActionChains(driver)

action_.move_to_element(t1)

# Double click to select whole field
action_.click(t1).pause(1)

# Press "delete" button to remove any string possibly present.
action_.send_keys(list(Keys.ARROW_DOWN)).pause(0.5)

action_.send_keys(list(Keys.ENTER))

action_.perform()


action_ = ActionChains(driver)

action_.move_to_element(ff_dd)


# Double click to select whole field
action_.double_click(death_year_from_to).pause(1)

# Press "delete" button to remove any string possibly present.
action_.send_keys(list(Keys.DELETE))

input_delay = wait_dist(len(year_str))


meta_df = hist_df.load_meta_data()

meta_df.dropna(inplace=True)

meta_df.drop_duplicates(
    subset=["country", "municipality", "year_from", "year_to"],
    keep="first",
    inplace=True,
    ignore_index=True,
)

meta_df.sort_values(
    ["country", "municipality", "year_from", "year_to"],
    inplace=True,
    na_position="last",
    ignore_index=True,
)


# .agg({"results_count": "max"})

t3 = meta_df.groupby(by=["country", "municipality", "year_from"])[
    "results_count"
].idxmax()

t4 = meta_df.loc[
    meta_df.groupby(by=["country", "municipality", "year_from"])[
        "results_count"
    ].idxmax()
]


dir(t3)
t3


t3.filter(lambda x: max(x) == x["results_count"])


dir(input_df)


class A:
    def __init__(self, test_df):
        self.test_df = test_df
        self.test_df.dropna(inplace=True)


a_inst = A(meta_df)

a_inst.test_df


hist_df.save_scrape_history()


assert isinstance(query_results := 5, int)


while True:
    records_df.scrape_elements()
    hist_df.save_scrape_history()
    nav_fs.scroll_down_page()
    nav_fs.next_page()
    sleep(2)


# %%


get_results_count_into_limit(1800, 1820)


meta_df = hist_df.load_meta_data()

meta_df.sort_values(
    ["country", "municipality", "year_from", "year_to"],
    inplace=True,
    na_position="last",
    ignore_index=True,
)


meta_df.drop_duplicates(
    subset=["country", "municipality", "year_from", "year_to"],
    keep="first",
    inplace=True,
    ignore_index=True,
)


assert t1 is not None, "Error"


t1 = None


init_results = nav_fs.get_filter_results()

nav_fs.year_to += 10

nav_fs.sidebar_more_options_selection()

increment_result = nav_fs.get_filter_results()

init_results - increment_result


while True:
    records_df.scrape_elements()
    nav_fs.scroll_down_page()
    nav_fs.next_page()
    sleep(2)

hist_df.save_scrape_history()


t1 = hist_df.load_scraped_history()


dir(hist_df)
hist_df.year_from = 30
nav_fs.event_munic
