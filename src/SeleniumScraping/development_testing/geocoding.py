"""Prepare data for export."""
from __future__ import annotations

# Standard Library
from typing import List

# Thirdparty Library
import numpy as np
import pandas as pd
import regex as re
from pandas.core.generic import NDFrame

# Package Library
from SeleniumScraping.driver.utils import print_method
from SeleniumScraping.parser.utils import columns_create, replace_whitespace
from SeleniumScraping.filepaths import FilePaths
re.DEFAULT_VERSION = re.V1

records_df = pd.read_feather(FilePaths.records_file)
records_df.fillna("", inplace=True)

def get_features(geo):
    """Get features from geodata."""
    if geo is None:
        return ["", np.nan, np.nan, np.nan]

    return [geo.address, geo.latitude, geo.longitude, geo.altitude]



pat_split = re.compile(r"\,\s", flags=re.REVERSE)


from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3

geolocator = GoogleV3(api_key=FilePaths.google_key, timeout=20, ssl_context=None)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2, max_retries=5)


def replace_whitespace(df_: str):
    df_copy = df_.copy()
    str_columns = df_copy.dtypes[
        df_copy.dtypes.isin(["O"])
    ].index.to_list()

    df_copy.fillna("", inplace=True)

    # Strip whitespaces and replace multiple whitespaces with a single one
    df_copy[str_columns] = df_copy.loc[:, str_columns].apply(
        lambda df_str: [" ".join(str_.split()) for str_ in df_str]
    )

    return df_copy




burial_columns = columns_create(records_df, "burial")

burial_columns2 = replace_whitespace(burial_columns)

query_df = burial_columns["burial_place"].drop_duplicates()



from time import sleep



geo_list = []

for idx, query_ in enumerate(query_df):

    geo = get_features(geocode([query_]))

    geo_list.append(geo)

    # Print current iteration step
    print(idx)

    # Sleep for 1 second
    sleep(1)


results_df = pd.DataFrame(geo_list, columns=["address", "lat", "lng", "alt"])






























column_date = "_".join([records_name, "date"])
column_place = "_".join([records_name, "place"])

# Split column into event place and event date in reversed order
split_cols = [
    re.split(
        r"(?<=\d+)\n", str_, flags=re.REVERSE, maxsplit=1, concurrent=True
    )
    for str_ in records_df[records_name]
]

records_split = pd.DataFrame(
    data=split_cols, columns=[column_place, column_date]
)



death_place = [pat_split.split(str_, concurrent=True) for str_ in records_split["death_place"]]

death_place = pd.DataFrame(death_place)

death_place.fillna("", inplace=True)





# Strip whitespaces and replace multiple whitespaces with a single one
death_place = death_place.apply(
    replace_whitespace
)


death_place.drop_duplicates(inplace=True)




