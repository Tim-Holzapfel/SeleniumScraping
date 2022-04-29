"""Unit tests."""
# Future Implementations
from __future__ import annotations

# Standard Library
import unittest

from secrets import choice

# Thirdparty Library
import pandas as pd

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.driver.history import HistoryData


class HistoryDataTest(unittest.TestCase):

    start_century = 1520
    end_century = 1920
    country = "Mexico"

    def test_case0(self):
        driver = TorBrowser(dev_mode=True)
        hist_df = HistoryData(driver)

        df_case_0 = pd.DataFrame(
            columns=[
                "country",
                "state",
                "municipality",
                "year_from",
                "year_to",
                "results_count",
                "page",
                "page_max",
            ]
        )

        hist_df.set_query_parameters(
            self.country, df_case_0, self.start_century, self.end_century
        )

    def test_case1(self):
        driver = TorBrowser(dev_mode=True)
        hist_df = HistoryData(driver)

        # Case 1: Unfinished pages
        country_case1 = "Mexico"
        state_case1 = "Aguascalientes"
        municipality_case1 = "Remos"
        year_from_case1 = 1710
        year_to_case1 = 1710
        page_case1 = 20
        page_max_case1 = 49

        df_case_1 = pd.DataFrame.from_dict(
            {
                "country": [country_case1],
                "state": [state_case1],
                "municipality": [municipality_case1],
                "year_from": [year_from_case1],
                "year_to": [year_to_case1],
                "results_count": [54824],
                "page": [page_case1],
                "page_max": [page_max_case1],
            }
        )

        hist_df.set_query_parameters(
            self.country, df_case_1, self.start_century, self.end_century
        )

        self.assertEqual(hist_df.year_from, 1710)
        self.assertEqual(hist_df.year_to, 1710)
        self.assertEqual(hist_df.page, page_case1 + 1)

    def test_case2(self):
        driver = TorBrowser(dev_mode=True)
        hist_df = HistoryData(driver)

        # Case 2: Year is bigger than 1700
        country_case2 = "Mexico"
        state_case2 = "Aguascalientes"
        municipality_case2 = "Remos"
        year_from_case2 = 1710
        year_to_case2 = self.end_century
        page_case2 = 49
        page_max_case2 = 49

        df_case_2 = pd.DataFrame.from_dict(
            {
                "country": [country_case2],
                "state": [state_case2],
                "municipality": [municipality_case2],
                "year_from": [year_from_case2],
                "year_to": [year_to_case2],
                "results_count": [54824],
                "page": [page_case2],
                "page_max": [page_max_case2],
            }
        )

        hist_df.set_query_parameters(
            self.country, df_case_2, self.start_century, self.end_century
        )

        self.assertEqual(hist_df.year_from, year_from_case2 - 1)
        self.assertEqual(hist_df.year_to, year_from_case2 - 1)
        self.assertEqual(hist_df.page, 1)

    def test_case3(self):
        driver = TorBrowser(dev_mode=True)
        hist_df = HistoryData(driver)

        # Case 3: Gaps in the timeframe

        country_case3 = "Mexico"
        state_case3 = "Aguascalientes"
        municipality_case3 = "Remos"
        year_from_case3 = self.start_century
        page_case3 = 49
        page_max_case3 = 49

        df_case_3 = pd.DataFrame.from_dict(
            {
                "country": [country_case3],
                "state": [state_case3],
                "municipality": [municipality_case3],
                "year_from": [year_from_case3],
                "year_to": [year_from_case3],
                "results_count": [54824],
                "page": [page_case3],
                "page_max": [page_max_case3],
            }
        )

        i = 0
        while df_case_3.loc[len(df_case_3) - 1, "year_to"] < self.end_century:
            i += 1
            df_case_3.loc[len(df_case_3) + 1] = {
                "country": "Mexico",
                "state": "Aguascalientes",
                "municipality": "Remos",
                "year_from": year_from_case3 + i,
                "year_to": year_from_case3 + i,
                "results_count": 54824,
                "page": page_case3,
                "page_max": page_max_case3,
            }
            df_case_3.reset_index(drop=True, inplace=True)

        idx_rnd = choice(df_case_3.index.to_list())

        year_drop = df_case_3.loc[idx_rnd, "year_from"]

        df_case_3.drop(index=idx_rnd, inplace=True)
        df_case_3.reset_index(drop=True, inplace=True)

        hist_df.set_query_parameters(
            self.country, df_case_3, self.start_century, self.end_century
        )

        self.assertEqual(hist_df.year_from, year_drop)
        self.assertEqual(hist_df.year_to, year_drop)
        self.assertEqual(hist_df.page, 1)

    def test_case4(self):
        driver = TorBrowser(dev_mode=True)
        hist_df = HistoryData(driver)

        # Case 4: Start new municipality
        country_case4 = "Mexico"
        state_case4 = "Aguascalientes"
        municipality_case4 = "Remos"
        year_from_case4 = self.start_century
        page_case4 = 49
        page_max_case4 = 49

        df_case_4 = pd.DataFrame.from_dict(
            {
                "country": [country_case4],
                "state": [state_case4],
                "municipality": [municipality_case4],
                "year_from": [year_from_case4],
                "year_to": [year_from_case4],
                "results_count": [54824],
                "page": [page_case4],
                "page_max": [page_max_case4],
            }
        )

        i = 0
        while df_case_4.loc[len(df_case_4) - 1, "year_to"] < self.end_century:
            i += 1
            df_case_4.loc[len(df_case_4) + 1] = {
                "country": "Mexico",
                "state": "Aguascalientes",
                "municipality": "Remos",
                "year_from": year_from_case4 + i,
                "year_to": year_from_case4 + i,
                "results_count": 54824,
                "page": page_case4,
                "page_max": page_max_case4,
            }
            df_case_4.reset_index(drop=True, inplace=True)

        hist_df.set_query_parameters(
            self.country, df_case_4, self.start_century, self.end_century
        )

        self.assertEqual(hist_df.year_from, self.start_century)
        self.assertEqual(hist_df.year_to, self.start_century)
        self.assertEqual(hist_df.page, 1)


# if __name__ == "__main__":
#    unittest.main()
