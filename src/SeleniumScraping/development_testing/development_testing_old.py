


type(pat_num)




nav_fs.reset_descriptors()


nav_fs.consent_button_clicked = True
#
# extensions.installDistroAddons
# extensions.getAddons.cache.enabled
# ---------------------------------------------------------------------- #
#                                Navigate                                #
# ---------------------------------------------------------------------- #

nav_fs.navigate_to_website_login()

nav_fs.website_login()

nav_fs.navigate_to_search()

hist_df.navigate_to_records()


#start Tor


tor_dir = FilePaths.tor_path.parent

tor_exe = FilePaths.tor_path.name

hist_df.click_consent_button()




import datetime




class DateFormat:
    """Format date."""

    def __init__(self):
        self._dmy_pat = re.compile(
            r"^\d{1,2}\s[A-Z][a-z]{3,}\s\d{4}$"
        )  # %d %B %Y
        self._dby_pat = re.compile(r"^\d{1,2}\s[A-Z][a-z]{2}\s\d{4}$") # "%d %b %Y
        self._my_pat = re.compile(r"^[A-Z][a-z]+\s\d{4}$")  # %B %Y
        self._y_pat = re.compile(r"^\d{4}$")  # %Y

    def _date_iso(self, date_str: str, date_format: str):
        return datetime.date.isoformat(
            datetime.datetime.strptime(date_str, date_format)
        )

    def _date_strp(self, date_str: str, date_format: str):
        return datetime.datetime.strptime(date_str, date_format)

    def __call__(self, date_str: str):
        """Format date."""
        if isinstance(date_str, str):
            return (
                self._date_strp(date_str, "%d %B %Y")
                if bool(self._dmy_pat.search(date_str))
                else self._date_strp(date_str, "%d %b %Y")
                if bool(self._dby_pat.search(date_str))
                else self._date_strp(date_str, "%B %Y")
                if bool(self._my_pat.search(date_str))
                else self._date_strp(date_str, "%Y")
                if bool(self._y_pat.search(date_str))
                else None
            )

        return date_str


data_format = DateFormat()















shp_path = "C:/Users/Tim/Desktop/New folder (2)/AFG_adm/AFG_adm1.shp"



from shapefile import Reader


shp_file = Reader(shp_path)



shp_iterator = shp_file.iterRecords()

type(shp_iterator)













for i in shp_iterator:
    t1 = i


type(t1)



type(t1.as_dict())



















date_ = "24 Apr 1712"





data_format(date_)


























scrape_hist = (
    pd.read_feather(FilePaths.history_file)
    .query(f"country == '{country}'")
)


scrape_hist = (
    pd.read_feather(FilePaths.history_file)
    .query(f"country == '{country}'")
    if history_file is None
    else history_file
)



dir(scrape_hist)




scrape_hist.query("country == 'Finland'")


scraped_data = load_scraped_data()


scraped_data.drop_duplicates()




df_records: pd.DataFrame = pd.read_feather(FilePaths.records_file)

df_records.drop_duplicates(inplace=True, ignore_index=True)

df_records.to_feather(FilePaths.records_file.as_posix())




import subprocess
dir(subprocess)


def _print(method: str, msg: str, *, color: str, sep: str = ": ") -> None:
    """Return print statement with the desired color."""
    method = colored(method, color, attrs=["bold"])
    print(method, msg, sep=sep)














procs_found = sum(
     [
         eq(str(FilePaths.tor_path), procs.info.get("exe"))
         for procs in process_iter(attrs=["exe"])
     ]
 )



tor_exe = start_tor()


import shutil

shutil.move("D://SeleniumScraping//src/SeleniumScraping//driver")




t1 = wait_dist(5)
type(t1)





print_method("start_tor", "I will try to start TOR now...")
java_kill()
tor_exe = Popen(FilePaths.tor_path)
tor_path = str(FilePaths.tor_path)

for procs in process_iter(["exe"]):
    t1 = procs.info.get("exe")

dir(t1)

t1.exe()


t1.info.get("exe")
t1.cwd()



print_method("start_tor", "I will try to start TOR now...")
java_kill()
tor_exe = Popen(FilePaths.tor_path)
tor_path = str(FilePaths.tor_path)
while True:
    procs_found = sum(
        [eq(tor_path, procs.info.get("exe")) for procs in process_iter(attrs=["exe"])]
    )
    if procs_found >= 4:
        print_method_success("start_tor", "I succesfully started TOR!")
        break
    print_method_error(
        "start_tor",
        f"I only found {procs_found} out of 4 processes. I will start looking again!",
    )
    sleep(1.5)
return tor_exe



dir(procs)


@func_set_timeout(timeout=80)
def start_tor() -> Popen:
    """Start Tor Browser."""
    print_method("start_tor", "I will try to start TOR now...")
    java_kill()
    tor_exe = Popen(FilePaths.tor_path)
    while True:
        procs_found = sum(
            [eq(str(FilePaths.tor_path), procs.exe()) for procs in process_iter(attrs=["exe"])]
        )
        if procs_found >= 4:
            print_method_success("start_tor", "I succesfully started TOR!")
            break
        print_method_error(
            "start_tor",
            f"I only found {procs_found} out of 4 processes. I will start looking again!",
        )
        sleep(1.5)
    return tor_exe

start_tor()
@atexit.register
def java_kill() -> None:
    r"""Terminate all processes associated with the scraping."""
    p_pat = re.compile(r"(jqs|javaw|java|geckodriver|phantomjs|firefox)\.exe")
    procs = process_iter(["name"])
    for process in procs:
        if bool(p_pat.match(process.name())):
            try:
                process.terminate()
            except NoSuchProcess:
                pass
    _, alive = wait_procs(procs, timeout=10)
    for process in alive:
        p_name = process.name()
        if bool(p_pat.match(p_name)):
            try:
                process.terminate()
            except NoSuchProcess:
                pass















dir(FilePaths.tor_path)


tor_exe = start_tor()

FilePaths.tor_path.as_uri()

tor_exe.terminate()
tor_exe.wait()




FilePaths.tor_path.absolute


dir(tor_exe)


tor_exe.returncode
tor_exe.pid



procs = process_iter(attrs=["exe", "pid"])

for process in procs:
    print(process.info)




tor_exe = subprocess.Popen(FilePaths.tor_path)
t1 = tor_exe.pid




for process in procs:
    if tor_path == process.info.get("exe"):  # type: ignore
        procs_found += 1



tor_path = str(FilePaths.tor_path)


from operator import eq





[eq(tor_path, procs.info.get("exe")) for procs in process_iter(attrs=["exe"])]



sum([eq(tor_path, procs.info.get("exe")) for procs in process_iter(attrs=["exe"])])







procs = process_iter(attrs=["exe"])
for process in procs:
    if str(FilePaths.tor_path) == process.info.get("exe")






















def print_iteration(n_iter: int, extra_iter: Optional[int] = None) -> None:
    """Print iteration seperator."""
    # Change iteration color at specific intervals
    iter_color = (
        "red"
        if (extra_iter is not None and n_iter % extra_iter == 0)
        else "grey"
    )

    iter_msg = " ".join([ordinal(n_iter), "Iteration"])
    os_size = get_terminal_size().columns - len(iter_msg)
    print_msg = "\r\n" + iter_msg + "-" * os_size + "\r\n"
    ctext = colored(print_msg, iter_color, attrs=["bold"])
    print(ctext)
    stdout.flush()






def print_msg(msg: str) -> None:
    msg = msg.upper()
    os_size = os.get_terminal_size().columns - len(msg)
    msg_fill = (os_size // 2) *  "#"
    print_msg = "\r\n" + msg_fill + msg + msg_fill + "\r\n"
    ctext = colored(print_msg, "grey", attrs=["bold"])
    print(ctext)
    stdout.flush()




print_msg("start preamble")
print_msg("end preamble")







os_size = get_terminal_size().columns - len(iter_msg)









print(socket.gethostbyname(socket.gethostname()))























feather_list = sorted(FilePaths.shapefiles_dir_user.rglob("*.feather"))

pat_feather = re.compile(r"^.*(?=\_admin\.feather)")



co_shapefiles = [pat_feather.findall(path_.name)[0].title().replace("_", " ") for path_ in feather_list]




len(pycountry.countries)
dir(pycountry)



pycountry.countries[0]







def outer_loop():
    i = 0
    j = 0
    while True:
        sleep(0.5)
        i += 1
        print(f"i: {i}")
        j += i
        inner_loop(j)

def inner_loop(j):
    # Loop 1
    while True:
        sleep(0.5)
        print(f"j: {j}")
        return
        if j == 10:
            return

outer_loop()









































pycountry.pycountry.ExistingCountries[0]



dir(pycountry.countries)
iso3 = pycountry.countries.lookup("Venezuela").alpha_3




s = requests.Session()
s.headers.update({'referer': "https://www.diva-gis.org/datadown"})
s.get(url, verify=False)



r = requests.get(url, stream=True, verify=False)

url = "https://biogeo.ucdavis.edu/data/diva/adm/AFG_adm.zip"












country = "Venezuela".title()

shp_exists = FilePaths.shapefiles_dir_user.joinpath(f"{country}_admin.feather").exists()

iso3 = pycountry.countries.lookup(country).alpha_3


temp_zip = NamedTemporaryFile(mode = "wb")

url = f"https://biogeo.ucdavis.edu/data/diva/adm/{iso3}_adm.zip"





def download_zip(zip_url: PathLike, zip_file: PathLike) -> None:
    # Download the file from the URL
    zipresp = urlopen(url)
    # Create a new file on the hard drive
    with open("D:/SeleniumScraping/test_zip.zip", "wb") as tempzip:
        # Write the contents of the downloaded file into the new file
        tempzip.write(zipresp.read())



































# %% Function start








dir(temp_dir)



co_shapefile = "Venezuela"






dir(shp_file_path)

shp_file_path.stem






dir("")

dir(pat_feather.search(t1[0].name))



search_button = driver.find_by_css("button[aria-controls='search']")

search_button.click()

sleep(1)

records_button = WebDriverWait(
    driver, timeout=15, poll_frequency=2
).until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "li[class='submenu-item '] a[data-test='records']")
    )
)

records_button.click()





dir(actions_)










records_button.is_displayed()


































driver.get("https://www.familysearch.org/en/")


href="/auth/familysearch/login?fhf=true&returnUrl=%2F"


sign_in_button = driver.find_button("a[href^='/auth/familysearch/']")



# %% Navigate

nav_fs.navigate_to_website_login()

nav_fs.website_login()

nav_fs.navigate_to_search()

hist_df.navigate_to_records()

# %% Main Part


@func_set_timeout(timeout=10)
def loop_inf():
    i = 0
    while True:
        sleep(1)
        print(i)
        i += 1



loop_inf()















t1.diff()








dir(t2)
list(t2)


for i in t2:
    print(i)


dir(act_profs)







n_iter = 5

iter_msg = " ".join([ordinal(n_iter), "Iteration"])

os_size = get_terminal_size().columns - len(iter_msg)

print(iter_msg + "-"*os_size + "\r")



ctext = colored(text, color, attrs=["bold"])

def print_iteration(n_iter: int) -> str:
    iter_msg = " ".join([ordinal(n_iter), "Iteration"])
    os_size = get_terminal_size().columns - len(iter_msg)
    print_msg = iter_msg + "-"*os_size + "\r"
    ctext = colored(print_msg, "grey", attrs=["bold"])
    print(ctext)
    sys.stdout.flush()











def print_colored(text: str, *, color: str) -> None:
    """Return print statement with the desired color."""
    text = " ".join(text.split())
    # text = re.sub(" +", " ", text.replace("\n", " ").strip())
    ctext = colored(text, color, attrs=["bold"])
    print(ctext, end="")


def print_method(method: str, msg: str, *, color: str = "blue") -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    # text = re.sub(" +", " ", text.replace("\n", " ").strip())
    method = colored(method, color, attrs=["bold"])
    print(method, msg, sep=": ", end="")

def print_descriptor(descriptor: str, msg: str, *, color: str = "yellow") -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    # text = re.sub(" +", " ", text.replace("\n", " ").strip())
    descriptor = colored(descriptor, color, attrs=["bold"])
    print(descriptor, msg, sep=" ", end="")




page_label_page = 5
page_label_max_page = 10


print_method(
    "get_current_page_number", f"Setting current page to {page_label_page} and page_max to {page_label_max_page}."
)


page_label_page = 5
page_label_max_page = 10
msg = f"Setting current page to {page_label_page} and page_max to {page_label_max_page}."

dir(msg)


msg.format_map()


msg.expandtabs()
colored(print_msg, "grey", attrs=["bold"])


msg = "test1: {test_value}"


re.sub("(\{[^\}]})",'colored(\1, "grey")',  msg)



colored("Scraping:", "blue")





bar_text = colored("Scraping: ", "blue", attrs=["bold"])

bar_len = 20

widgets=[
    bar_text, progressbar.Counter(), " of ", str(bar_len),
    progressbar.PercentageLabelBar(),
    ' (', progressbar.ETA(), ') ',
]
for i in progressbar.progressbar(range(20), widgets=widgets):
    time.sleep(0.1)


dir(progressbar)








msg = f"test3"

msg2 = " ".join(msg.split())






for i in range(200):
    print_iteration(i)
    if i % 20 == 0:
        print(i)





frozenset({"from __future__ import print_function"})



def get_page(self, peek: bool = False) -> int:
    """Get current page as integer."""
    # Current property value of the page element at the bottom of the page
    # which equals the current page number as reported by dynamic input element
    page_input_page = int(driver.find_by_css("div[pageno] input").get_property("value"))

    # Page label reporting the current page and the total number of pages at
    # the bottom of the page
    page_label = driver.find_by_css(
        "button[aria-label^='Go to next Page']"
    ).get_attribute("aria-label")

    # Regular expression extracting all numbers from the page label
    # at the bottom of the page
    page_label_regex = re.findall("\\d+", page_label)

    # The page label MUST contain exactly two numbers: the current page and the
    # total number of pages. Otherwise something IS wrong.
    assert len(page_label_regex) == 2, "The page label did not report exactly two numbers."

    # Current page taken from the page label at the bottom of the page
    page_label_page = int(page_label_regex[0])

    # Maximum number of pages for the given query taken from the page label at the
    # bottom of the page
    page_label_max_page = int(page_label_regex[1])

    # Test to make sure that the current page is equal to the url page
    try:
        # Current page as taken from the current url of the website. NOTE:
        # familysearch.org starts the page count in the url at zero at not at one.
        # To account for that the `url_page` has to be increased by one.
        page_url_page = (
            int(
                furl(driver.current_url).query.params[
                    "offset"
                ]  # type: ignore
            )
            // 100
            + 1
        )
        # If the current page is also the first page the url is not going to
        # contain an "offset" parameter which is, however, crucial for determining
        # the current page using the url. Hence, if an "KeyError" is raised due to
        # the absence of an "offset" parameter then it is reasonable to assume
        # that the current page is the first page (page "1").
    except KeyError:
        page_url_page = 1

    # Because we always set the number of results per page to 100, that means that
    # the total number of pages for the current search MUST equal the number of
    # total results for the current query divided by 100. If the division contains
    # an remainder than the total number of pages is going to be equal to the
    # ceiling of the division with the last page containing the division's
    # remainder. NOTE: Because familysearch.org introduced a page limit of 49
    # pages per query, the total number of pages needs to be capped at 49, which
    # is why the min() function is included.
    page_logic_max_page = min([49, ceil(nav_fs.get_filter_results() / 100)])

    assert page_logic_max_page == page_label_max_page, "The maximum number of pages as reported by the page label is not the same as the logical total number of pages."

    assert page_input_page == page_url_page, "The current page as reported by the page label is not the same as url page."

    if not peek:
        self.page = page_label_page
        self.page_max = page_label_max_page
        print(
            f"get_current_page_number: Setting current page to {self.page}"
        )

    return page_label_page





results_con = driver.find_by_css("#resultsContainer")


driver.execute_script(
     "return arguments[0].scrollTop;", results_con
)




button_css = "input[aria-describedby='page-number']"

page_css = driver.find_by_css(button_css)



page_css.location





def scroll_down_page() -> None:
    """Scroll page down to the footer."""
    # Results table element
    results_con = driver.find_by_css("#resultsContainer")

    # Max possible scroll
    scroll_max = driver.execute_script(
         "return arguments[0].scrollTopMax;", results_con
    )

    # Focus results table
    driver.execute_script("arguments[0].focus();", results_con)

    while True:
        # Send a "page down" keystroke
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

        # Retrieve current position on page
        current_scroll = driver.execute_script(
             "return arguments[0].scrollTop;", results_con
        )

        # Check if current scroll has been exhausted
        if current_scroll == scroll_max:
            break


        sleep(wait_dist(1, 0.8).item())



scroll_down_page()




results_con = driver.find_by_css("#resultsContainer")


page_root = driver.find_by_css(":root")

driver.execute_script(
     "return arguments[0].scrollTop;", page_root
)

driver.execute_script(
     "return arguments[0].scrollTopMax;", page_root
)




x1 = driver.execute_script(
     "return arguments[0].scrollTop;", page_root
)

ActionChains(driver).send_keys(Keys.PAGE_UP).perform()


x2 = driver.execute_script(
     "return arguments[0].scrollTop;", page_root
)

ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

x3 = driver.execute_script(
     "return arguments[0].scrollTop;", page_root
)


ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

x4 = driver.execute_script(
     "return arguments[0].scrollTop;", page_root
)




x4 - x3

x3 - x2

x2 - x1




(x4 - x3)/x4


(x3 - x2)/x3









def scroll_main_page(scroll_direction: Literal["up", "down"] = "down") -> None:
    """Scroll main element of page up or down."""

    key_dir = Keys.PAGE_DOWN if scroll_direction == "down" else Keys.PAGE_UP

    # Results table element
    page_root = driver.find_by_css(":root")

    # Max possible scroll
    scroll_max = driver.execute_script(
        "return arguments[0].scrollTopMax;", page_root
    )

    # Focus main page
    driver.execute_script("arguments[0].focus();", page_root)

    # Decide which value should be targeted: if the scroll direction is up
    # then the target value should be 0 as 0 means the top of the scroll bar
    # otherwise it should be scroll_max.
    scroll_opt = scroll_max if scroll_direction == "down" else 0

    current_scroll = driver.execute_script(
        "return arguments[0].scrollTop;", page_root
    )

    while current_scroll != scroll_opt:
        # Send either a page up or down keystroke
        ActionChains(driver).send_keys(key_dir).perform()

        # Retrieve current position on page
        current_scroll = driver.execute_script(
            "return arguments[0].scrollTop;", page_root
        )

        sleep(wait_dist(1, 0.8).item())




scroll_main_page("up")







with ProgressBar(max_value=100) as p_bar:
    for i in range(100):
        sleep(0.5)
        p_bar.update(i)

warnings.warn("Warning...........Message")


dir(warnings)

def scroll_inner_page(
    scroll_direction: Literal["up", "down"] = "down"
) -> None:
    """Scroll inner page either up or down."""
    key_dir = (
        Keys.PAGE_DOWN if scroll_direction == "down" else Keys.PAGE_UP
    )

    # Results table element
    results_con = driver.find_by_css("#resultsContainer")

    # Max possible scroll
    scroll_max = driver.execute_script(
        "return arguments[0].scrollTopMax;", results_con
    )

    # Focus results table
    driver.execute_script("arguments[0].focus();", results_con)

    # Decide which value should be targeted: if the scroll direction is up
    # then the target value should be 0 as 0 means the top of the scroll bar
    # otherwise it should be scroll_max.
    scroll_opt = scroll_max if scroll_direction == "down" else 0

    # Retrieve current position on page
    current_scroll = driver.execute_script(
        "return arguments[0].scrollTop;", results_con
    )


    scroll_prog = ProgressBar(max_value=scroll_max, initial_value=current_scroll)


    with scroll_prog as p_bar:
        while current_scroll != scroll_opt:
            # Send a "page down" keystroke
            ActionChains(driver).send_keys(key_dir).perform()

            # Retrieve current position on page
            current_scroll = driver.execute_script(
                "return arguments[0].scrollTop;", results_con
            )

            sleep(wait_dist(1, 0.8).item())
            p_bar.update(current_scroll)



scroll_inner_page("up")



results_con.get_attribute("class")


results_fixed = driver.find_by_css("#resultsContainer > div[format='fixedTable']")




driver.execute_script("arguments[0].focus();", results_con)



driver.execute_script(
     "return arguments[0].scrollTop;", results_con
)

driver.execute_script(
     "return arguments[0].scrollTopMax;", results_con
)






driver.execute_script(
     "return arguments[0].scrollHeight;", results_fixed
)




current_pos = driver.execute_script(
     "return arguments[0].scrollTop;", results_con
)



current_pos1 = driver.execute_script(
     "return arguments[0].scrollHeight;", results_con
)

driver.execute_script(
     "return arguments[0].offsetHeight;", results_con
)



driver.execute_script(
     "return arguments[0].scrollY;", results_con
)




driver.execute_script(
     "return window.scrollMaxY;"
)













action_ = ActionChains(driver)

action_.send_keys(Keys.PAGE_DOWN)

action_.move_to_element(results_con)

action_.perform()




def scroll_down_page(self, anchor_css: str) -> None:
    """Scroll page down to the footer."""


    while True:
        # Element to use as an "anchor position" while scrolling down the
        # page
        anchor_element = self.driver.find_by_css(anchor_css)

        # Position of anchor element (y-axis)
        anchor_pos = anchor_element.location["y"]

        # Send a "page down" keystroke
        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()

        # Retrieve current position on page
        current_pos: float = self.driver.execute_script(
            "return window.pageYOffset;"
        )

        # Check if anchor element has been reached
        if (current_pos + 800) >= anchor_pos:
            # Make sure the element is within the viewport
            anchor_element.location_once_scrolled_into_view
            break
        sleep(wait_dist(1, 0.8).item())



def move_to_page(self, page_num: int) -> None:
    """Move to specified page number."""
    # Inner window containing the main scroll abr
    results_con = self.driver.find_by_css("#resultsContainer > div[format='fixedTable']")

    # Move to inner window. Otherwise a "pae down" keystroke will be send
    # to the outer scroll bar and not the inner one.
    ActionChains(self.driver).move_to_element(results_con).perform()

    # Page anchor
    page_sel_css = "input[aria-describedby='page-number']"

    self.scroll_down_page(page_sel_css)

    page_selection = self.driver.find_by_css(page_sel_css)

    actions_ = ActionChains(self.driver)

    actions_.move_to_element(page_selection).pause(1)
    actions_.double_click(page_selection).pause(1)
    actions_.send_keys(list(str(page_num))).pause(1)
    actions_.send_keys(list(Keys.ENTER)).pause(1)
    actions_.perform()

    self.check_page_loaded()



hist_df.scroll_down_page('button[aria-label*="Go to next Page"]')


t1 = driver.find_by_css('button[aria-label*="Go to next Page"]')
t1.location_once_scrolled_into_view




hist_df.move_to_page(20)


hist_df.next_page()


t1 = furl(driver.current_url).query

type(t1)
type(t1.params)

type(furl(driver.current_url))



anchor_css = "input[aria-describedby='page-number']"

anchor_pos = driver.find_by_css(anchor_css)



ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()




anchor_pos.location_once_scrolled_into_view


def scroll_down_page(anchor_css: str) -> None:
    """Scroll page down to the footer."""
    while True:
        # Element to use as an "anchor position" while scrolling down the page
        anchor_element = driver.find_by_css(anchor_css)

        # Position of anchor element (y-axis)
        anchor_pos = anchor_element.location["y"]

        # Send a "page down" keystroke
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

        # Retrieve current position on page
        current_pos: float = driver.execute_script(
            "return window.pageYOffset;"
        )

        # Check if anchor element has been reached
        if (current_pos + 800) >= anchor_pos:
            # Make sure the element is within the viewport
            anchor_pos.location_once_scrolled_into_view
            break
        sleep(wait_dist(1, 0.8).item())




scroll_down_page("input[aria-describedby='page-number']")





anchor_pos.accessible_name




dir(anchor_pos)















nav_fs.check_page_loaded()

scrape_history.drop(columns="created_at", inplace=True)



scrape_history.drop(index=25, inplace=True)



scrape_history.to_feather(FilePaths.history_file)




scrape_history = load_scraped_history()


scrape_history.loc[1, "year_from"] = 1700
scrape_history.loc[1, "year_to"] = 1700


scrape_history.query("year_from == 1700 & year_from >= 1700")

scrape_history.drop(index = 1, inplace=True)

scrape_history.reset_index(drop=True, inplace=True)





hist_df.set_query_parameters("mexico")















100 // 100 + 1


dict_messages = collections.defaultdict(dict)



dict_messages["negative"][2] = [
            """
            Perfect, we are back on track! Refreshing worked and the bot
            check is gone.
            """,
        ]



type(dict_messages)




page_source = driver.page_source

with open("C:/Users/Tim/Desktop/records_source.html","w") as f:
    f.write(page_source)

scrape_hist_sub = scrape_history.groupby(["country", "state", "municipality"])["year_from"].min().reset_index().query("year_from > 1700").reset_index(drop=True)



scrape_hist_sub.loc[0, ["country", "state", "municipality"]]



hist_df.get_page(peek=True)













def wheel_element(element, deltaY = 120, offsetX = 0, offsetY = 0):
  error = element._parent.execute_script("""
    var element = arguments[0];
    var deltaY = arguments[1];
    var box = element.getBoundingClientRect();
    var clientX = box.left + (arguments[2] || box.width / 2);
    var clientY = box.top + (arguments[3] || box.height / 2);
    var target = element.ownerDocument.elementFromPoint(clientX, clientY);

    for (var e = target; e; e = e.parentElement) {
      if (e === element) {
        target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
        return;
      }
    }
    return "Element is not interactable";
    """, element, deltaY, offsetX, offsetY)
  if error:
    raise WebDriverException(error)



results_con = driver.find_by_css(".css-1slb4r")

results_con.get_attribute("format")


wheel_element(results_con, 120)




dir(action_)

from selenium.webdriver.remote.webdriver import

selenium.webdriver.



dir(events)




Keys.DOWN
Keys.



driver.execute_script("window.scrollTo(-30,document.body.scrollHeight)")

results_element = driver.find_element_by_css_selector("#resultsContainer")



driver.execute_script("arguments[0].focus();", results_element)

action_ = ActionChains(driver)
action_.send_keys(Keys.PAGE_DOWN).perform()








def scroll_down_page(self, anchor_css: str) -> None:
    """Scroll page down to the footer."""

    # Results table element
    results_con = self.driver.find_by_css(
        "#resultsContainer"
    )

    # Focus results table
    driver.execute_script("arguments[0].focus();", results_element)


    while True:
        # Element to use as an "anchor position" while scrolling down the
        # page

        anchor_element = self.driver.find_by_css(anchor_css)

        # Send a "page down" keystroke
        ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()

        # Position of anchor element (y-axis)
        anchor_pos = anchor_element.location["y"]

        # Retrieve current position on page
        current_pos: float = self.driver.execute_script(
            "return window.pageYOffset;"
        )

        # Check if anchor element has been reached
        if (current_pos + 800) >= anchor_pos:
            # Make sure the element is within the viewport
            break
        sleep(wait_dist(1, 0.8).item())







nav_fs.scroll_down_page('button[aria-label*="Go to next Page"]')

















results = driver.find_element_by_link_text("Filter Results (298,830,638)")

results_test = driver.find_element_by_css_selector("h5.css-1jpzde6")
results_test.text
# %% Testing Area








#resultsContainer > div > div:nth-child(1) > div > div > div.css-1ssbn0c > div > h5





















































# +31653224315
# Netherlands



blacklist_df = pd.read_feather(FilePaths.blacklist_path)
blacklist_df.loc[len(blacklist_df) + 1] = {
    "sms_number": "+31653224315",
    "sms_country": "Netherlands"
    }
blacklist_df.drop_duplicates(inplace=True)
blacklist_df.reset_index(drop=True, inplace=True)
blacklist_df.to_feather(FilePaths.blacklist_path)


config["PHONE"]["phone_number"]










dir(FilePaths)



blacklist_df = pd.read_feather(FilePaths.blacklist_path)


sms_df = pd.read_feather(FilePaths.sms_df_user)



pd_df = pd.read_feather(FilePaths.sms_df_user)

blacklist_df = pd.read_feather(FilePaths.blacklist_path)


t1 = set(pd_df.sms_number).difference(blacklist_df.sms_number)

dir(pd_df)
t_ind = pd_df.index.difference(blacklist_df.index)


t2 = pd_df.iloc[t_ind]


dir(t1)
+31653224315
+31653224315
sms_




pd_df = pd_df.merge(right=blacklist_df, how="left", indicator=True).query("_merge=='left_only'").drop(columns="_merge")
