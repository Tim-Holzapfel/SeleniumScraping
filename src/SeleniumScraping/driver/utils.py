"""Utility functions."""

# Future Implementations
from __future__ import annotations

# Standard Library
import atexit
import collections

from datetime import datetime
from functools import singledispatch
from os import get_terminal_size
from secrets import choice
from subprocess import Popen
from time import perf_counter
from typing import (
    Any,
    DefaultDict,
    Generator,
    List,
    Literal,
    Optional,
)

# Thirdparty Library
import pandas as pd
import regex as re
import win32con
import win32gui

from func_timeout import func_set_timeout
from numpy import dtype, float64, ndarray
from numpy.random import default_rng
from psutil import NoSuchProcess, process_iter, wait_procs
from termcolor import colored

# Package Library
from SeleniumScraping.filepaths import FilePaths


@func_set_timeout(timeout=80)
def start_tor(t_max: int = 80) -> Popen[bytes]:
    """Start Tor Browser."""
    print_method("start_tor", "I will try to start TOR now...")
    java_kill()
    tor_exe = Popen(FilePaths.tor_path)

    proc_list: List[str] = []

    def enum_callback(
        hwnd: str,
        extra: Optional[Any] = None,  # pylint: disable=unused-argument
    ) -> None:
        """Enumerate callback function."""
        tor_pat = re.compile(r"^About\sTor.*Tor\sBrowser$")
        if bool(tor_pat.search(win32gui.GetWindowText(hwnd))):
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            proc_list.append(hwnd)

    t_start = perf_counter()
    while True:
        win32gui.EnumWindows(enum_callback, None)
        diff_t = round(t_max - (perf_counter() - t_start), 1)
        print_counter(
            "start_tor",
            f"I'm waiting for TOR to start...({diff_t}s until timeout)",
            color="red",
        )
        if any(proc_list):
            print("")
            print_method_success("start_tor", "I successfully started TOR!")
            break

    return tor_exe


@atexit.register
def java_kill() -> None:
    """Terminate all processes associated with the scraping."""
    p_pat = re.compile(r"(jqs|javaw|java|geckodriver|phantomjs|firefox)\.exe")
    for process in (procs := process_iter(["name"])):
        proc_name = process.info.get("name")
        assert isinstance(proc_name, str)
        if bool(p_pat.match(proc_name)):
            try:
                process.terminate()
            except NoSuchProcess:
                pass
    _, alive = wait_procs(procs, timeout=10)
    for process in alive:
        p_name = process.info.get("name")
        assert isinstance(p_name, str)
        if bool(p_pat.match(p_name)):
            try:
                process.terminate()
            except NoSuchProcess:
                pass


def ordinal(n_int: int) -> str:
    """Print ordinal number.

    Parameters
    ----------
    n_int : int
        Number to print.

    Returns
    -------
    str
        Initial number as string with the appropriate suffix.
    """
    ord_num = f"{n_int}{'tsnrhtdd'[(n_int // 10 % 10 != 1) * (n_int % 10 < 4) * n_int % 10 :: 4]}"
    return ord_num


@singledispatch
def wait_dist(
    n_size: int | str, mean_wait: int | float = 0.2
) -> ndarray[Any, dtype[float64]]:
    """Array of seconds for the browser to wait.

    Parameters
    ----------
    n_size : int, str
        Number of wait times to generate. If supplied value is a string then
        the number of generated wait times will be equal to the string length.
    mean_wait : int, float, optional
        Mean of the normal distribution which will be used for the generation
        of the wait times. The default is 0.2.

    Raises
    ------
    NotImplementedError
        If `n_size` has a type different than str or int.

    Returns
    -------
    ndarray
        Numpy array of generated wait times.
    """
    raise NotImplementedError("Unsupported type")


@wait_dist.register(int)
def _(
    n_size: int, mean_wait: int | float = 0.2
) -> ndarray[Any, dtype[float64]]:
    return abs(default_rng().normal(loc=1 / 6, scale=mean_wait, size=n_size))


@wait_dist.register(str)
def _(
    n_size: str, mean_wait: int | float = 0.2
) -> ndarray[Any, dtype[float64]]:
    str_len = len(n_size)
    return abs(default_rng().normal(loc=1 / 6, scale=mean_wait, size=str_len))


def print_con(msg: str) -> None:
    """Print continued lines as a single line."""
    msg_split = " ".join(msg.split())
    print(msg_split, flush=True)


def print_fatal_error(msg: str):
    """Print Fatal Error Message."""
    msg = " ".join(msg.split())
    msg_split = colored(
        msg, color="red", on_color="on_yellow", attrs=["underline", "bold"]
    )
    print(msg_split, flush=True)


def print_special(
    method: str,
    msg: str,
) -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    method = colored(method, "magenta", attrs=["bold"])
    print(method, msg, sep=": ", flush=True)


def print_method(
    method: str,
    msg: str,
) -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    method = colored(method, "blue", attrs=["bold"])
    print(method, msg, sep=": ", flush=True)


def print_method_success(
    method: str,
    msg: str,
) -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    method = colored(method, "green", attrs=["bold"])
    print(method, msg, sep=": ", flush=True)


def print_method_error(
    method: str,
    msg: str,
) -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    method = colored(method, "red", attrs=["bold"])
    print(method, msg, sep=": ", flush=True)


def print_descriptor(
    method: str,
    msg: str,
) -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    method = colored(method, "yellow", attrs=["bold"])
    print(method, msg, sep=" ", flush=True)


def print_counter(method: str, msg: str, color: str = "blue") -> None:
    """Return print statement with the desired color."""
    msg = " ".join(msg.split())
    method = colored(method, color, attrs=["bold"])
    print("\r" + method + ": " + msg + "\r", end="", sep="", flush=True)


def print_section_heading(msg: str) -> None:
    """Print custom message to screen."""
    msg = msg.upper()
    os_size = get_terminal_size().columns - len(msg)
    msg_fill = (os_size // 2) * "#"
    msg_print = "\r\n" + msg_fill + msg + msg_fill + "\r\n"
    ctext = colored(msg_print, "grey", attrs=["bold"])
    print(ctext, flush=True)


def print_iteration(n_iter: int, extra_iter: Optional[int] = None) -> None:
    """Print iteration seperator."""
    iter_time = (
        datetime.now()
        .strftime("%A, %d %B %Y - %I:%M:%S %p")
        .lstrip("0")
        .replace(" 0", " ")
    )
    # Change iteration color at specific intervals
    iter_color = (
        "magenta"
        if (extra_iter is not None and n_iter % extra_iter == 0)
        else "grey"
    )

    iter_msg = " ".join([ordinal(n_iter), "Iteration:", iter_time])
    os_size = get_terminal_size().columns - len(iter_msg)
    msg_print = "\r\n" + iter_msg + "-" * os_size + "\r\n"
    ctext = colored(msg_print, iter_color, attrs=["bold"])
    print(ctext, flush=True)


def to_snakecase(input_str: str) -> str:
    """Replace string with snakecase."""
    return_str = re.sub(r"[\-\s]", "_", str(input_str))
    return_str = re.sub(r":", "", return_str)

    return return_str.lower()


def validate_input(input_msg: str) -> bool:
    """Validate user input."""
    user_input = input(" ".join([input_msg, "[Yes/No]:"]))

    while user_input not in ["Yes", "No"]:
        user_input = input("Please enter either Yes or No.")

    return_input = user_input == "Yes"

    return return_input


# -------------------------------------------------------------------------- #
#                      Convenience data loading functions                    #
# -------------------------------------------------------------------------- #


def load_scraped_history() -> pd.DataFrame:
    """Load scraped history data file."""
    hist_df: pd.DataFrame = pd.read_feather(FilePaths.history_file)

    return hist_df


# -------------------------------------------------------------------------- #
#                              Botcheck messages                             #
# -------------------------------------------------------------------------- #


class Messages(object):
    """Botcheck test messages."""

    def __init__(self) -> None:
        """Botcheck test messages."""
        self.arg_tuple: tuple[
            Literal["negative", "positive"], int
        ] | None = None
        dict_messages: DefaultDict[
            Literal["negative", "positive"], dict[int, List[str]]
        ] = collections.defaultdict(dict)
        dict_messages["negative"][1] = [
            """
            Phew, no bot check yet!
            """,
        ]
        dict_messages["negative"][2] = [
            """
            Perfect, we are back on track! Refreshing worked and the bot
            check is gone.
            """,
        ]
        dict_messages["negative"][3] = [
            """
            Finally! The bot check is gone, it was about high time.
            """,
        ]
        dict_messages["positive"][1] = [
            """
            Damn it! Familysearch invoked a bot check.
            I will refresh the website, usually this solves it.
            """,
            """
            Ugh! Now they invoked a botcheck...
            I will refresh the website, usually this solves it.
            """,
        ]
        dict_messages["positive"][2] = [
            """
            Cut me a break! Alright, that didn't work.
            Let me try refreshing the website one more time to see if
            I can get rid of that bot check.
            """,
        ]
        dict_messages["positive"][3] = [
            """
            It's no use, I will need to restart the browser to get
            rid of the bot check.
            """,
        ]

        for key in dict_messages:
            sub_key = dict_messages[key]
            for sub_sub_key in sub_key:
                msg_list = sub_key[sub_sub_key]
                msg_list = [" ".join(msg_.split()) for msg_ in msg_list]
                sub_key[sub_sub_key] = msg_list

        self.dict_messages = dict_messages

    def __get__(
        self,
        arg_tuple: object | None,
        arg_type: Optional[type[object]] = None,
    ) -> str | None:
        """Print event message."""
        if self.arg_tuple is None:
            return None
        outcome = self.arg_tuple[0]
        counter = self.arg_tuple[1]
        return_msg = choice(self.dict_messages[outcome][counter])
        return return_msg

    def __set__(
        self,
        arg_tuple: object,
        value: tuple[Literal["negative", "positive"], int],
    ) -> None:
        """Set message parameters."""
        if self.arg_tuple is None:
            return None
        assert isinstance(
            value, tuple
        ), "Supplied argument must be of type list."
        assert value[0] in [
            1,
            2,
            3,
        ], "The 'counter' argument must be either 1, 2 or 3."
        assert value[1] in [
            "positive",
            "negative",
        ], "The outcome argument must be either 'positive' or 'negative'."
        self.arg_tuple = value


def all_str(test_object: pd.Series) -> bool:
    """Test if all elements of `test_object` are pf type str.

    Parameters
    ----------
    test_object : pd.Series
        Series which elements need to best tested.
    """

    def _help_fun() -> Generator[bool, None, None]:
        for str_ in test_object:
            yield isinstance(str_, str)

    return all(list(_help_fun()))
