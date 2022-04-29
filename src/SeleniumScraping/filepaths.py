"""File paths used within the project."""

# Future Implementations
from __future__ import annotations

# Standard Library
from configparser import ConfigParser
from os import getenv
from pathlib import Path
from typing import cast

# Thirdparty Library
import pandas as pd

from importlib_resources import files
from webdrivermanager import GeckoDriverManager


class FilePaths(object):
    """Project specific paths to files."""

    # ---------------------------------------------------------------------- #
    #                            Base Directories                            #
    # ---------------------------------------------------------------------- #

    # NOTE: even though the return value of "files" is "Traversable", "files"
    # actually returns "WindowsPath" (on Windows) or more generally "Path"
    internal_dir = cast(Path, files("SeleniumScraping"))

    root_dir = internal_dir.parents[1]

    user_home_dir = getenv("USERPROFILE")
    assert isinstance(user_home_dir, str)

    user_roaming_dir = getenv("APPDATA")
    assert isinstance(user_roaming_dir, str)

    # (Internal) Data Directory

    data_dir_internal = internal_dir / "data"
    data_dir_internal.mkdir(exist_ok=True)

    addons_dir = data_dir_internal / "addons"
    addons_dir.mkdir(exist_ok=True)

    settings_file = root_dir / "settings.ini"

    if settings_file.exists():
        config = ConfigParser()
        config.read(settings_file)
        google_key = config["KEYS"]["google_key"]

    # ---------------------------------------------------------------------- #
    #                    (User) Directory containing data                    #
    # ---------------------------------------------------------------------- #

    data_dir_user = Path(user_roaming_dir) / "SeleniumScraping"
    data_dir_user.mkdir(exist_ok=True)

    shapefiles_dir_user = data_dir_user / "shapefiles"
    shapefiles_dir_user.mkdir(exist_ok=True)

    spacy_dir_user = data_dir_user / "spacy"
    spacy_dir_user.mkdir(exist_ok=True)

    spacy_models_dir = spacy_dir_user / "models"
    spacy_models_dir.mkdir(exist_ok=True)

    user_error_log = data_dir_user / "error_log.log"

    # Path to the dataframe containing SMS data
    sms_df_user = data_dir_user / "sms_df.feather"

    # Dataframe with SMS numbers that are not working
    # (familysearch.org didn't send an activation code to)
    blacklist_path = data_dir_user / "sms_blacklist.feather"

    if not blacklist_path.exists():
        sms_blacklist_df = pd.DataFrame(columns=["sms_number", "sms_country"])
        sms_blacklist_df.reset_index(drop=True, inplace=True)
        sms_blacklist_df.to_feather(blacklist_path.as_posix())

    # Path to the exported Stata file
    stata_export_path = data_dir_user / "records_data.dta"

    # ---------------------------------------------------------------------- #
    #          (User) Directory containing familysearch.org Profiles         #
    # ---------------------------------------------------------------------- #

    profile_dir_user = data_dir_user / "profiles"
    profile_dir_user.mkdir(exist_ok=True)

    # Profiles that have not yet been activated
    inactive_profs_dir_user = profile_dir_user / "inactive"
    inactive_profs_dir_user.mkdir(exist_ok=True)

    # Profiles that are already active and are ready for deployment
    active_profs_dir_user = profile_dir_user / "active"
    active_profs_dir_user.mkdir(exist_ok=True)

    country_syms_user = data_dir_user / "country_synonyms_user.feather"

    if not country_syms_user.exists():
        # Python cannot save an empty dictionary as a feather file so the
        # dictionary must be initialized with at least one entry.
        sym_dict = dict({"Russia": ["Russian Federation"]})
        pd.DataFrame.from_dict(data=sym_dict).to_feather(country_syms_user)

    # ---------------------------------------------------------------------- #
    #                 (User) Directory containing executables                #
    # ---------------------------------------------------------------------- #

    exe_dir_user = data_dir_user / "executables"
    exe_dir_user.mkdir(exist_ok=True)

    geckodriver_path = exe_dir_user / "geckodriver.exe"

    if not geckodriver_path.exists():
        gdd = GeckoDriverManager(
            download_root=exe_dir_user,
            link_path=exe_dir_user,
            os_name="win",
        )
        gdd.download_and_install()

    # (User) Googlemaps queries

    query_dir = data_dir_user / "queries"
    query_dir.mkdir(exist_ok=True)

    # ---------------------------------------------------------------------- #
    #                    (User) Export Directory                             #
    # ---------------------------------------------------------------------- #

    export_dir_user = getenv("export_dir")
    assert isinstance(
        export_dir_user, str
    ), """Environment variable 'export_dir is not defined.
    Please set the environment variable.'"""

    export_dir_user_path = Path(export_dir_user)

    # ---------------------------------------------------------------------- #
    #                    (Internal) Path to the TOR binary                   #
    # ---------------------------------------------------------------------- #

    desktop_path_user = Path(user_home_dir) / "Desktop"

    tor_path = desktop_path_user / "Tor Browser" / "Browser" / "firefox.exe"

    # ---------------------------------------------------------------------- #
    #                         (Internal) History File                        #
    # ---------------------------------------------------------------------- #

    history_file = data_dir_user / "history_file.feather"

    if not history_file.exists():
        hist_df = pd.DataFrame(
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
        hist_df.reset_index(drop=True, inplace=True)
        hist_df.to_feather(history_file.as_posix())

    # ---------------------------------------------------------------------- #
    #                         (Internal) Records File                        #
    # ---------------------------------------------------------------------- #

    records_dir = data_dir_user / "records"
    records_dir.mkdir(exist_ok=True)
