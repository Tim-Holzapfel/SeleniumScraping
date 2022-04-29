"""Container for the scraped data."""

# Future Implementations
from __future__ import annotations

# Standard Library
from collections import defaultdict
from typing import TYPE_CHECKING

# Thirdparty Library
import pandas as pd
import regex as re

from progressbar import ETA, Counter, PercentageLabelBar, progressbar
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from termcolor import colored

# Package Library
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.utils import (
    print_method,
    print_special,
    to_snakecase,
)
from SeleniumScraping.filepaths import FilePaths


if TYPE_CHECKING:
    # Package Library
    from SeleniumScraping.base import TorBrowser


class RecordsData(Navigate):
    """Class for storing scraped data."""

    def __init__(
        self,
        driver: TorBrowser,
    ) -> None:
        """Initialize class.

        Parameters
        ----------
        driver : TorBrowser
            DESCRIPTION.

        Returns
        -------
        None.
        """
        self.driver = driver
        self.pat_misc_key = re.compile(r"^.*\:")
        super().__init__(driver)

    def load_records(self) -> str:
        """Load record data."""
        assert isinstance(self.event_country, str)

        # Normalized country name
        country_norm = (
            pd.Series(self.event_country)
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8", errors="ignore")
            .str.lower()
            .str.replace(" ", "_")
            .to_list()[0]
        )

        # File path for records data
        feather_path = (
            FilePaths.records_dir / f"records_{country_norm}.feather"
        )

        if not feather_path.exists():
            df_records = pd.DataFrame(
                index=range(0),
                columns=["death", "birth", "burial"],
            )
            df_records.reset_index(drop=True, inplace=True)
            df_records.to_feather(feather_path.as_posix())

        return feather_path.as_posix()

    def scrape_elements(self):
        """Scrape elements from familysearch.org."""
        self.botcheck_test()

        # Get path to the records file
        records_path = self.load_records()

        df_records: pd.DataFrame = pd.read_feather(records_path)

        table_body = self.driver.find_by_css(
            "#resultsContainer > div > div:nth-child(2) > table > tbody"
        )

        table_cells: list[WebElement] = table_body.find_elements(
            By.CSS_SELECTOR, "tr"
        )

        return_dict: dict[str, dict[str, str]] = defaultdict(dict)

        bar_text = colored("Scraping: ", "blue", attrs=["bold"])

        table_len = len(table_cells)

        widgets = [
            bar_text,
            Counter(),
            " of ",
            str(table_len),
            " Records ",
            PercentageLabelBar(),
            " (",
            ETA(),
            ") ",
        ]

        for i in progressbar(range(table_len), widgets=widgets):
            t_cell = table_cells[i]
            # Name for the dictionary that is created for the current
            # records entry
            d_name = f"{i:03}"

            # -------------------------------------------------------------- #
            #                        Keyword Elements                        #
            # -------------------------------------------------------------- #

            key_elements = t_cell.find_elements(By.CSS_SELECTOR, "strong")

            key_list = [t_key.text for t_key in key_elements]

            pat_keys = [r"(?<=\n|^)" + str_ + r"(?!\s)" for str_ in key_list]

            # The `first_key_pos` marks the text position where the first part
            # of the text, which does not use keywords and needs to be treated
            # differently than the the second part, ends, and the second part
            # beginns.

            # Text before first keyword appears with empty elements removed
            first_key_pos = re.search(
                f"{pat_keys[0]}",
                t_cell.text,
                flags=re.S,
            ).start()  # type: ignore

            # -------------------------------------------------------------- #
            #                 Text first half dictionary loop                #
            # -------------------------------------------------------------- #

            text_first_half = list(
                filter(None, t_cell.text[:first_key_pos].split("\n"))
            )

            t_len = len(text_first_half)

            for idx, text_ in enumerate(text_first_half):
                value_ = text_
                if idx == 0:
                    key_ = "respondent_name"
                elif idx == (t_len - 2):
                    key_ = "respondent_role"
                elif idx == (t_len - 1):
                    key_ = "collection_name"
                elif bool(_key := self.pat_misc_key.findall(text_)[0]):
                    key_ = to_snakecase(_key.group(0))
                    value_ = self.pat_misc_key.sub("", text_).strip()
                else:
                    continue

                return_dict[d_name][key_] = value_

            # -------------------------------------------------------------- #
            #                Text second half dictionary loop                #
            # -------------------------------------------------------------- #

            # Text after first keyword appears
            text_second_half = t_cell.text[first_key_pos:]

            # dictionary values for the second half of the text
            value_list = list(
                filter(None, re.split("|".join(pat_keys), text_second_half))
            )

            for key_, value_ in zip(key_list, value_list):
                key_snake = to_snakecase(key_)
                return_dict[d_name][key_snake] = value_

        # ------------------------------------------------------------------ #
        #                  Append dict to existent dataframe                 #
        # ------------------------------------------------------------------ #

        df_records_ext = pd.DataFrame.from_dict(
            return_dict,
            orient="index",
        ).reset_index(drop=True)

        df_records = df_records.append(df_records_ext, ignore_index=True)

        try:
            # Number of duplicated records
            dups_count = df_records.duplicated().value_counts().loc[True]
            print_special(
                "scrape_elements",
                f"I'm removing {dups_count} duplicated records from the DataFrame!",
            )

            # Remove duplicated entries from the DataFrame.
            df_records.drop_duplicates(inplace=True, ignore_index=True)
        except KeyError:
            pass

        # Replace old records DataFrame with the "new" one, basically just
        # appending the records that were scraped just now to the already
        # existing records.
        df_records.to_feather(records_path)

        msg_ = f"""
            I successfully scraped page {self.page} of
            {self.event_munic}, {self.event_state}, {self.event_country}!
            The DataFrame already contains {len(df_records)} entries!
            """

        msg_ = " ".join(msg_.split())

        print_method("scrape_elements", msg_)

        return df_records_ext
