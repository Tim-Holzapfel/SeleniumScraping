"""Scrape familysearch."""

# Future Implementations
from __future__ import annotations

# Standard Library
import logging
import os

# Thirdparty Library
from func_timeout import FunctionTimedOut
from selenium.common.exceptions import TimeoutException

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.descriptors import validate_country
from SeleniumScraping.driver.history import HistoryData
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.records import RecordsData
from SeleniumScraping.driver.shapefiles import ShapeFiles
from SeleniumScraping.driver.utils import (
    print_fatal_error,
    print_iteration,
    print_method_error,
    print_section_heading,
    print_special,
)
from SeleniumScraping.exceptions import InvalidISOError, ProfileError
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.parser.processing import Processing


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=FilePaths.user_error_log,
    filemode="w",
)


# Es geht um Schweden, Finnland, Tschechien, Estland.

# Falls möglich, auch Russland, Ukraine, Polen, Deutschland, Frankreich (dies
# sind weniger wichtig u. vermutlich riesig)

# Ich bin besonders interessiert an death registers der Zeit (Geburtsjahre)
# 1500-1800, für Finnland bis 1850, also Sterbejahre von ca. 1550 bis 1890.


def main(
    country: str,
    idx: int,
    nav_fs: Navigate,
    hist_df: HistoryData,
    records_df: RecordsData,
    data_export: Processing,
    export_rate: int,
    prof_change_rate: int,
) -> None:
    """Initialize the scraping procedure.

    Parameters
    ----------
    country : str
        Country to scrape.
    headless : bool, optional
        Run Firefox without a Graphical User Interface. The default is False.
    export_rate : int, optional
        Number of iterations after which the dataset will be exported.
        The default is 20.
    prof_change_rate : int, optional
        Number of iterations after which the user profile will be changed.
        The default is 40.

    Returns
    -------
    None.
    """
    country = validate_country(country).name
    ShapeFiles(country)

    while True:
        # ------------------------------------------------------------------ #
        #                              Navigate                              #
        # ------------------------------------------------------------------ #

        print_section_heading("start navigation")
        nav_fs.navigate_to_website_login()

        nav_fs.website_login()

        nav_fs.navigate_to_search()

        hist_df.navigate_to_records()
        print_section_heading("end navigation")
        # ------------------------------------------------------------------ #
        #                              Scraping                              #
        # ------------------------------------------------------------------ #
        while True:
            # Retrieve and set the query arguments necessary for the
            # familysearch query
            hist_df.set_query_parameters(country)

            # Set preference in "advanced search" to "all information"
            nav_fs.set_preferences_to_all_information()

            # Summon the more options side page and enter the previously set
            # query arguments
            hist_df.start_search_query()

            # If the page should contain no results then continue to the next
            # page
            if hist_df.no_results_found:
                hist_df.save_scrape_history()
                continue

            # If the page retrieved by `set_query_parameters` is not 1 that
            # means that the scraping of the specific event-place/event-time
            # combination was interrupted and stopped before all pages were
            # scraped. In this case we will go to the page where we last left
            # off
            if hist_df.page != nav_fs.get_page(peek=True):

                # Scroll down to the page end and set current page equal to
                # the page where we last left off
                nav_fs.move_to_page(hist_df.page)

            else:
                # If the page retrieved by `set_query_parameters` is equal to
                # 1 then the current search query is saved to the search query
                # history
                hist_df.save_scrape_history()

            # If the current page is not also the last page of the current
            # query then scrape all pages until we have reached the last page
            while hist_df.page != hist_df.page_max:
                idx += 1
                print_iteration(idx, prof_change_rate)
                if idx % export_rate == 0:
                    data_export()
                if idx % prof_change_rate == 0:
                    print_special(
                        "prof_change",
                        "It's about time to change the profile.",
                    )
                    hist_df.reset_descriptors()
                    return

                # Scrape the records displayed on the current page
                records_df.scrape_elements()

                # Replace the page number of the scrape history for the
                # current municipality with the current page number to mark
                # the current page in the scrape history record as finished
                hist_df.update_scrape_history_page()

                # Scroll down to the page end and navigate to the next page
                nav_fs.next_page()

            idx += 1
            print_iteration(idx, prof_change_rate)
            if idx % export_rate == 0:
                data_export()
            if idx % prof_change_rate == 0:
                print_special(
                    "prof_change", "It's about time to change the profile."
                )
                hist_df.reset_descriptors()
                return

            # If the current page should also be the last page of the current
            # query then we only need to scrape the page and update the scrape
            # history without the other two steps

            # Scrape the records displayed on the current page
            records_df.scrape_elements()

            # Update scrape history
            hist_df.update_scrape_history_page()


def main_loop(
    country: str,
    headless: bool = True,
    export_rate: int = 250,
    prof_change_rate: int = 500,
    cent_start: int = 1520,
    cent_end: int = 1890,
) -> None:
    """Run the main function in an infinity loop."""
    # Clear console
    os.system("cls")
    # Set color scheme for console
    os.system("color FF")
    idx = 0
    while True:
        try:
            driver = TorBrowser(headless=headless)
            nav_fs = Navigate(driver)
            hist_df = HistoryData(
                driver=driver, cent_start=cent_start, cent_end=cent_end
            )
            records_df = RecordsData(driver)
            data_export = Processing(driver)
        except OSError:
            continue
        try:
            # -------------------------------------------------------------- #
            #                        Init main classes                       #
            # -------------------------------------------------------------- #
            main(
                nav_fs=nav_fs,
                idx=idx,
                hist_df=hist_df,
                records_df=records_df,
                data_export=data_export,
                country=country,
                export_rate=export_rate,
                prof_change_rate=prof_change_rate,
            )
        except KeyboardInterrupt:
            return
        except ProfileError:
            print_method_error(
                "ProfileError",
                "The profile was invalid and I had to start over again.",
            )
        except TimeoutError:
            print_method_error(
                "TimeoutError",
                "One of the operations timed out, I had to start over again.",
            )
        except TimeoutException:
            print_method_error(
                "TimeoutException",
                "One of the operations timed out, I had to start over again.",
            )
        except FunctionTimedOut as exc:
            print_fatal_error(exc.msg)
        except InvalidISOError as exc:
            print_fatal_error(exc.errors)
            return
        # except:
        #    last_error = sys.exc_info()[2]
        #    traceback.print_tb(last_error, limit=5)
        finally:
            driver.close_browser()
            hist_df.reset_descriptors()


if __name__ == "__main__":
    # Standard Library
    import doctest

    doctest.testmod()
