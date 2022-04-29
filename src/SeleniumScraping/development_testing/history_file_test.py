"""Load municipality dataframe and cache it for later use."""

# Thirdparty Library
import numpy as np
import pandas as pd

# Package Library
from SeleniumScraping.driver.filepaths import FilePaths


country = "Mexico"


# Make sure that the supplied country is always in lower case
country = country.lower()

# Set datapath pointing to the current file of interest
data_path = FilePaths.admin_dir.joinpath(f"{country}_admin.feather")

# Load municipalities for the scraping.
df_mu = pd.read_feather(data_path)

df_mu.sort_values(
    ["state", "municipality"],
    inplace=True,
    na_position="last",
    ignore_index=True,
)

df_mu["municipality"] = [
    pat_arrow_brac.search(mun_).group(0)
    if pat_arrow_brac.search(mun_) is not None
    else mun_
    for mun_ in df_mu["municipality"]
]

df_mu["municipality"] = [
    pat_no_brac.search(mun_).group(0).strip()
    if pat_no_brac.search(mun_) is not None
    else mun_
    for mun_ in df_mu["municipality"]
]
