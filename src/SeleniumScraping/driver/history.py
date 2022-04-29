"""Container for the scrape history."""

# Future Implementations
from __future__ import annotations

# Standard Library
from functools import cache
from typing import TYPE_CHECKING, Optional

# Thirdparty Library
import pandas as pd

from pandas.core.generic import NDFrame

# Package Library
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.utils import print_method
from SeleniumScraping.filepaths import FilePaths


if TYPE_CHECKING:
    # Package Library
    from SeleniumScraping.base import TorBrowser


class HistoryData(Navigate):
    """Container for the scrape history and results count meta data."""

    def __init__(
        self, driver: TorBrowser, cent_start: int = 1519, cent_end: int = 1920
    ):
        """Initialize history class.

        Parameters
        ----------
        driver : TorBrowser
            DESCRIPTION.
        cent_start : int, optional
            Lower bound of the year search range. The default is 1519.
        cent_end : int, optional
            Upper bound of the year search range. The default is 1920.
        """
        self.driver = driver
        self.cent_start = cent_start
        self.cent_end = cent_end
        super().__init__(driver)

    @cache
    def load_municipalities(self, country: str) -> pd.DataFrame:
        """Load municipality dataframe and cache it for later use."""
        # Make sure that the supplied country is always in lower case
        country = country.lower()

        # Set datapath pointing to the current file of interest
        data_path = FilePaths.shapefiles_dir_user.joinpath(
            f"{country}_admin.feather"
        )

        # Load municipalities for the scraping.
        df_mu = pd.read_feather(data_path)

        df_mu.sort_values(
            ["state", "municipality"],
            inplace=True,
            na_position="last",
            ignore_index=True,
        )

        return df_mu

    def set_query_parameters(
        self, country: str, history_file: Optional[NDFrame] = None
    ) -> None:
        """Set query parameters for the search query.

        Parameters
        ----------
        country : str
            Country in which to search for records.
        history_file : NDFrame, optional
            History file to use. The default is None.

        Raises
        ------
        ValueError
            If the year range was specified incorrectly.

        Returns
        -------
        None.
        """
        scrape_hist = (
            pd.read_feather(FilePaths.history_file).query(
                f"country == '{country}'"
            )
            if history_file is None
            else history_file
        )

        # Set of years that should be scraped for every municipality.
        full_range = set(range(self.cent_start, self.cent_end + 1))

        # ------------------------------------------------------------------ #
        #                Case 0: No Scrape history exists yet                #
        # ------------------------------------------------------------------ #

        if len(scrape_hist) == 0:

            print_method(
                "set_query_parameters",
                "Case 0 applied! (no dataset found / starting new data)",
            )

            munic_df = self.load_municipalities(country)

            (
                self.event_country,
                self.event_state,
                self.event_munic,
            ) = munic_df.loc[0, ["country", "state", "municipality"]]

            self.page = 1

            self.year_from, self.year_to = self.cent_start, self.cent_start

            return

        # ------------------------------------------------------------------ #
        #             Case 1: Municipality with unfinished pages             #
        # ------------------------------------------------------------------ #

        # Should there exist yet unfinished queries then we should first
        # finish them

        if len(scrape_hist_sub := scrape_hist.query("page != page_max")) >= 1:

            print_method(
                "set_query_parameters", "Case 1 applied! (Unfinished pages)"
            )

            (
                self.event_country,
                self.event_state,
                self.event_munic,
            ) = scrape_hist_sub.iloc[0][["country", "state", "municipality"]]

            self.year_to = self.year_from = int(
                scrape_hist_sub.iloc[0][["year_to"]]
            )

            page = int(scrape_hist_sub.iloc[0][["page"]]) + 1

            # NOTE: It is important that the page where we last left off shown
            # in the records is within the page range of the current search
            # meaning that the page we are going to set does not exceed the
            # number of pages currently available

            # Retrieve page and page_max of current search
            self.get_page(verbose=False)

            assert isinstance(self.page_max, int)

            self.page = self.page_max if self.page_max < page else page

            return

        # ------------------------------------------------------------------ #
        #                        Case 2: Missing years                       #
        # ------------------------------------------------------------------ #

        for name, group in scrape_hist.groupby(
            ["country", "state", "municipality"]
        )["year_from"]:
            # NOTE: The first intersection is important because it restricts
            # the year range to the bounds of `cent_start` and `cent_end` or
            # put differently: the intersection prevents an infinite loop in
            # case that group should contain a year that is not within the
            # range of `cent_start` and `cent_end`.
            _group = set(group).intersection(full_range)
            if (
                len(missing_years := full_range.symmetric_difference(_group))
                != 0
            ):
                print_method(
                    "set_query_parameters",
                    "Case 2 applied! (Missing years)",
                )

                self.year_from = self.year_to = int(list(missing_years)[0])
                self.event_country, self.event_state, self.event_munic = name
                self.page = 1
                return

        # ------------------------------------------------------------------ #
        #                 Case 3: Start with new municipality                #
        # ------------------------------------------------------------------ #

        print_method(
            "set_query_parameters",
            "Case 3 applied! (starting new municipality)",
        )
        munic_df = self.load_municipalities(country)

        # NOTE: the following computation is valid even if the scrape history
        # dataframe is empty!
        scrape_hist_sub = (
            scrape_hist.groupby(["country", "state", "municipality"])[
                "year_to"
            ]
            .max()
            .reset_index()
        )

        assert isinstance(scrape_hist_sub, pd.DataFrame)

        # Based on the scrape history: remove all rows for which a scrape
        # history was found with a "year_to" value greater than 1900.
        munic_df_sub = (
            munic_df.merge(
                right=scrape_hist_sub,
                how="left",
                on=["country", "state", "municipality"],
            )
            .query(
                f"year_to < {self.cent_end} | year_to.isnull()",
                engine="python",
            )
            .drop(columns="year_to")
            .reset_index(drop=True)
        )

        (
            self.event_country,
            self.event_state,
            self.event_munic,
        ) = munic_df_sub.loc[0, ["country", "state", "municipality"]]

        self.year_from, self.year_to = self.cent_start, self.cent_start

        self.page = 1

    def save_scrape_history(self) -> NDFrame:
        """Save scrape meta data including the results count.

        Returns
        -------
        NDFrame.
        """
        assert (
            self.event_country is not None
        ), "save_scrape_history: Country is not set."
        assert (
            self.event_munic is not None
        ), "save_scrape_history: event_munic is not set."
        assert (
            self.event_state is not None
        ), "save_scrape_history: Municipality is not set."
        assert (
            self.year_from is not None
        ), "save_scrape_history: year_from is not set."
        assert (
            self.year_to is not None
        ), "save_scrape_history: year_to is not set."

        # Write current page number, country and time to the scraping
        # history file.

        df_hist = pd.read_feather(FilePaths.history_file)

        query_results = self.get_filter_results()

        assert isinstance(
            query_results, int
        ), "save_scrape_history: could not retrieve filter results!"

        if self.no_results_found:
            df_hist.loc[len(df_hist)] = {
                "country": self.event_country,
                "state": self.event_state,
                "municipality": self.event_munic,
                "year_from": self.year_from,
                "year_to": self.year_to,
                "results_count": 0,
                "page": 1,
                "page_max": 1,
            }
        else:
            self.get_page()

            df_hist.loc[len(df_hist)] = {
                "country": self.event_country,
                "state": self.event_state,
                "municipality": self.event_munic,
                "year_from": self.year_from,
                "year_to": self.year_to,
                "results_count": query_results,
                "page": 0,
                "page_max": self.page_max,
            }

        df_hist = self.sort_dataframe(df_hist)

        df_hist.to_feather(FilePaths.history_file)

        print_method("save_scrape_history", "History saved!")

        return df_hist

    def update_scrape_history_page(self) -> None:
        """Update the page index of the scrape history file.

        Returns
        -------
        None.
        """
        assert (
            self.event_country is not None
        ), "save_scrape_history: Country is not set."
        assert (
            self.event_munic is not None
        ), "save_scrape_history: event_munic is not set."
        assert (
            self.event_state is not None
        ), "save_scrape_history: Municipality is not set."
        assert (
            self.year_from is not None
        ), "save_scrape_history: year_from is not set."
        assert (
            self.year_to is not None
        ), "save_scrape_history: year_to is not set."

        df_hist = pd.read_feather(FilePaths.history_file)

        hist_idx = df_hist.query(
            "&".join(
                [
                    f"country == '{self.event_country}'",
                    f"state == '{self.event_state}'",
                    f"municipality == '{self.event_munic}'",
                    f"year_from == {self.year_from}",
                    f"year_to == {self.year_to}",
                ]
            )
        ).index.values[0]

        print_method(
            "update_scrape_history_page", f"Updated history to {self.page}!"
        )

        self.get_page(verbose=False)

        df_hist.loc[hist_idx, "page"] = self.page

        df_hist.loc[hist_idx, "page_max"] = self.page_max

        df_hist.to_feather(FilePaths.history_file)

    def sort_dataframe(self, input_df: pd.DataFrame) -> NDFrame:
        """Sort Dataframe.

        Parameters
        ----------
        input_df : pd.DataFrame
            DataFrame to be modified.
        ex_cols : Sequence[str], str, optional
            String or Sequence of column names to exclude while sorting value
            and dropping duplicates. The default is None.

        Returns
        -------
        output_df : TYPE
            The supplied DataFrame but without duplicate columns and sorted
            rows.
        """
        output_df = input_df.copy(deep=True)

        scrape_cols = (
            output_df.columns.drop("results_count")
            .to_series()
            .reset_index(drop=True)
        )

        rep_dic = {
            "country": True,
            "state": True,
            "municipality": True,
            "year_from": True,
            "year_to": True,
            "page": False,
            "page_max": True,
        }

        asc_sort_order = scrape_cols.replace(to_replace=rep_dic)

        sort_cols = scrape_cols.to_list()

        output_df.sort_values(
            by=sort_cols,
            ascending=asc_sort_order,
            inplace=True,
            na_position="last",
            ignore_index=True,
        )

        dup_cols = [
            "country",
            "state",
            "municipality",
            "year_from",
            "year_to",
        ]

        output_df.drop_duplicates(
            subset=dup_cols,
            keep="first",
            inplace=True,
            ignore_index=True,
        )

        return output_df
