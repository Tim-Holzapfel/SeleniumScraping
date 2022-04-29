"""Generate a user account."""

# Future Implementations
from __future__ import annotations

# Standard Library
from calendar import month_name, monthrange
from configparser import ConfigParser
from datetime import date, datetime
from secrets import choice, randbelow, token_urlsafe

# Thirdparty Library
import regex as re

# Package Library
from SeleniumScraping.descriptors import PhoneIter
from SeleniumScraping.driver.utils import FilePaths
from SeleniumScraping.names import get_first_name, get_last_name


class User:
    """Generate profile."""

    sms_gen = PhoneIter()

    def __init__(self):
        self._c_year = date.today().year
        self.pat_num = re.compile(r"\d+")
        self.prof_name_list = None
        self.prof_gen_count = 0
        self.ini_pat = "*.ini"

    def gen_prof_name_list(self, num_profs: int):

        act_prof_list = sorted(
            FilePaths.active_profs_dir_user.rglob(self.ini_pat)
        )

        inactive_prof_list = sorted(
            FilePaths.inactive_profs_dir_user.rglob(self.ini_pat)
        )

        prof_list = act_prof_list + inactive_prof_list

        prof_set = {
            int(self.pat_num.findall(prof_.name)[0]) for prof_ in prof_list
        }

        num_profs = len(prof_set) + num_profs + 1

        num_list = set(list(range(1, num_profs)))

        prof_set.symmetric_difference_update(num_list)

        self.prof_name_list = list(prof_set)

    def generate_birthday(self) -> tuple[str, str, str, str]:
        """Generate random birthday for user profile."""
        # Choose a year so that the user is at least 18 but not older than 80.
        year_birth: int = choice(
            range((self._c_year - 80), (self._c_year - 17))
        )
        # Choose a random month for the birthday
        month_birth_int: int = choice(range(1, 13))

        # Get number of days for given month in given year in order to account
        # for leap years.
        num_days: int = monthrange(year_birth, month_birth_int)[1]

        # Choose a random day in the given month.
        day_birth = str(choice(range(1, num_days + 1)))

        month_birth_chr = month_name[month_birth_int]

        return (
            str(year_birth),
            str(month_birth_int),
            month_birth_chr,
            day_birth,
        )

    def generate_user_identity(self):
        """Generate user information."""
        # User gender. The non-binary choice is not offered by familysearch.org
        gender: str = choice(["female", "male"])

        # Generate random first name of the selected gender.
        first_name: str = get_first_name(gender=gender)

        # Generate random last name.
        last_name: str = get_last_name()

        return gender, first_name, last_name

    def generate_profile(self) -> None:
        """Generate random user information."""
        # %% Write user information to a configuration file.
        config = ConfigParser()

        config["GENERAL"] = {}  # type: ignore
        gen_info = config["GENERAL"]
        gen_info["created_at"] = str(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )

        gender, first_name, last_name = self.generate_user_identity()

        (
            year_birth,
            month_birth_int,
            month_birth_chr,
            day_birth,
        ) = self.generate_birthday()

        config["USER"] = {}  # type: ignore
        user_info = config["USER"]
        user_info["gender"] = gender
        user_info["first_name"] = first_name
        user_info["last_name"] = last_name
        user_info["year_birth"] = year_birth
        user_info["month_birth_int"] = month_birth_int
        user_info["month_birth_chr"] = month_birth_chr
        user_info["day_birth"] = day_birth

        # %% Load SMS File
        sms_number, sms_country = self.sms_gen

        # %% Phonenumber information
        config["PHONE"] = {}  # type: ignore
        user_phone = config["PHONE"]
        user_phone["phone_number"] = sms_number
        user_phone["phone_country"] = sms_country
        user_phone[
            "phone_website"
        ] = f"https://receive-smss.com/sms/{sms_number[1:]}"

        # %% Account information
        config["ACCOUNT"] = {}  # type: ignore
        acc_info = config["ACCOUNT"]

        # %%% Generate Password
        acc_info["password"] = token_urlsafe()

        # %% Generate username

        # Generate random combination of numbers.
        number = f"{randbelow(99999):05d}"
        user_name = first_name + "_" + last_name + "_" + number

        acc_info["name"] = user_name

        acc_info["activated"] = "False"

        assert isinstance(self.prof_name_list, list)
        prof_name = self.prof_name_list[self.prof_gen_count]

        self.prof_gen_count += 1

        prof_file = (
            FilePaths.inactive_profs_dir_user / f"profile{prof_name}.ini"
        )

        with open(prof_file, "w", encoding="UTF-8") as configfile:
            config.write(configfile)

    def get_num_profs(self, status_inactive: bool = True) -> int:
        """Return number of created profiles.

        Parameters
        ----------
        status_inactive : bool, optional
            Return number of inactive profiles. The default is True.

        Returns
        -------
        int
            Number of profiles found.
        """
        profile_path = (
            FilePaths.inactive_profs_dir_user
            if status_inactive
            else FilePaths.active_profs_dir_user
        )

        return len(list(profile_path.rglob(self.ini_pat)))

    def profile_factory(self, max_profs: int) -> None:
        """Create the specified number of profiles."""

        self.gen_prof_name_list(max_profs)

        num_profs = self.get_num_profs()

        while True:
            if num_profs >= max_profs:
                break
            self.generate_profile()
            num_profs += 1
