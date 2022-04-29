"""Activating user profile."""

# Future Implementations
from __future__ import annotations

# Package Library
from SeleniumScraping.base import TorBrowser
from SeleniumScraping.exceptions import (
    NoFlagFoundError,
    NoSMSCodeError,
    ProfileError,
)
from SeleniumScraping.filepaths import FilePaths
from SeleniumScraping.generate.account import RegisterUser
from SeleniumScraping.generate.user import User


def main(reg_inst: RegisterUser) -> None:
    """Generate and activate user profiles."""
    # Read profile information
    reg_inst.read_profile()

    # Navigate to first page
    reg_inst.first_page()

    # Navigate to second page
    reg_inst.second_page()


def main_loop(num_profs: int = 20) -> None:
    """Start loop."""
    if not FilePaths.sms_df_user.exists():
        driver_sms = TorBrowser(onion_network=False)
        driver_sms.get_sms()

    # Instantiate user class
    user_inst = User()

    # Generate as many profiles as specified
    user_inst.profile_factory(num_profs)

    # Count number of active profiles
    num_active_profs = user_inst.get_num_profs(False)

    while num_active_profs < num_profs:
        # Start Tor Browser
        driver_tor = TorBrowser()

        # Start Firefox browser
        driver_sms = TorBrowser(onion_network=False)

        # Instantiate user class
        reg_inst = RegisterUser(driver_tor, driver_sms)
        try:
            main(reg_inst)
            num_active_profs = user_inst.get_num_profs(False)
        except ProfileError:
            # If a profile error exists then delete the profile and continue
            # with the next iteration
            continue
        except NoFlagFoundError:
            continue
        except NoSMSCodeError:
            continue
        finally:
            reg_inst.reset_descriptors()
            driver_sms.close_browser()
            driver_tor.close_browser()


if __name__ == "__main__":
    main_loop()
