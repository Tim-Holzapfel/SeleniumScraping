"""Container for the scraped data."""
from __future__ import annotations

# Standard Library
from collections import defaultdict
from typing import TYPE_CHECKING, List

# Thirdparty Library
import pandas as pd
import regex as re
from progressbar import progressbar
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

# Package Library
from SeleniumScraping.driver.navigate import Navigate
from SeleniumScraping.driver.utils import to_snakecase
from SeleniumScraping.filepaths import FilePaths


if TYPE_CHECKING:
    # Package Library
    from SeleniumScraping.base import TorBrowser


# -------------------------------------------------------------------------- #
#                                Records Data                                #
# -------------------------------------------------------------------------- #

driver = TorBrowser()


_dmy_pat = re.compile(r"^\d{1,2}\s[A-Z][a-z]+\s\d{4}$")
_my_pat = re.compile(r"^[A-Z][a-z]+\s\d{4}$")
_y_pat = re.compile(r"^\d{4}$")
_date_pat = re.compile(
            r"(January|February|March|April|May|June|July|August|September|October|November)?\s?\d{4}$"
        )

_val_pat = re.compile(
            r"(?<=Birth|Death|Burial|Father\:|Mother\:|Spouse\:).*", flags=re.S
        )
_key_pat = re.compile(
            r"(Birth|Death|Burial|Father|Mother|Spouse)", flags=re.S
        )
pat_gender = re.compile(r"Sex\:")
pat_misc_key = re.compile(r"^.*\:")


"""Scrape elements from familysearch.org."""


df_records: pd.DataFrame = pd.read_feather(FilePaths.records_file)

table_body = driver.find_by_css(
    "#resultsContainer > div > div:nth-child(2) > table > tbody"
)

table_cells: List[WebElement] = table_body.find_elements(
    By.CSS_SELECTOR, "tr"
)

return_dict: defaultdict[str, dict[str, str]] = defaultdict(dict)


i = 35


for i in progressbar(range(len(table_cells))):
    t_cell = table_cells[i]
    # Name for the dictionary that is created for the current
    # records entry
    d_name = f"{i:03}"

    # --------------------------------------------------------------- #
    #                               Dictionary Keys                   #
    # --------------------------------------------------------------- #

    key_elements = t_cell.find_elements(By.CSS_SELECTOR, "strong")

    key_list = [t_key.text for t_key in key_elements]

    pat_keys = [r"(?<=\n|^)" + str_ + r"(?!\s)" for str_ in key_list]

    # The `first_key_pos` marks the text position where the first part of the text,
    # which does not use keywords and needs to be treated differently than the
    # the second part, ends, and the second part beginns.
    # Text before first keyword appears with empty elements removed

    first_key_pos = re.search(
        f"{pat_keys[0]}", t_cell.text, flags=re.S
    ).start()


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
        elif bool(_key := pat_misc_key.search(text_)):
            key_ = to_snakecase(
                _key.group(0)
            )
            value_ = pat_misc_key.sub("", text_).strip()
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
    return_dict,  # type: ignore
    orient="index",
)

df_records_ext.reset_index(drop=True, inplace=True)

df_records = df_records.append(df_records_ext, ignore_index=True)

df_records.to_feather(FilePaths.records_file.as_posix())

msg_ = f"""
    I successfully scraped page {self.page} of
    {self.event_munic}, {self.event_state}, {self.event_country}!
    """

msg_ = " ".join(msg_.split())

print(msg_)

return df_records_ext
