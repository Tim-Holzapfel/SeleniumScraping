"""Command line parser."""

# Future Implementations
from __future__ import annotations

# Standard Library
import argparse
import sys

from collections.abc import Callable
from typing import Optional

# Package Library
from SeleniumScraping.driver.main import main_loop as scrape_main
from SeleniumScraping.driver.utils import java_kill
from SeleniumScraping.generate.main import main as generate_main
from SeleniumScraping.parser.processing import parser_records_export
from SeleniumScraping.parser.utils import get_prev_scraped_country


def main_parser():
    """Command line parser."""
    # ---------------------------------------------------------------------- #
    #                               Main Parser                              #
    # ---------------------------------------------------------------------- #
    # %% Main Parser
    parser = argparse.ArgumentParser(
        prog="SeleniumScraping",
        description="""
        The command can be executed by typing '%(prog)s' followed by either
        'account', 'scrape' or 'export'. For example '%(prog)s' would
        open the current .ini file and '%(prog)s export' would export the
        scraped data records as a Stata file. The commands are described in
        more detail below.
        """.replace(
            "\n", " "
        ),
    )

    subparsers = parser.add_subparsers(
        prog="SeleniumScraping", required=True, title="Available Commands"
    )

    # ---------------------------------------------------------------------- #
    #                             Account Parser                             #
    # ---------------------------------------------------------------------- #
    parser_account = subparsers.add_parser(
        name="account",
        add_help=True,
        help="""
            Create a familysearch.org account. However, before it is
            necessary to adjust the .ini file by calling '%(prog)s open'
        """.replace(
            "\n", ""
        ),
    )

    parser_account.add_argument(
        "num_profs",
        type=int,
        nargs="?",
        default=40,
        help="""Number of profiles to generate.""".replace("\n", " "),
    )

    parser_account.set_defaults(func=generate_main)

    # ---------------------------------------------------------------------- #
    #                             Export Parser                              #
    # ---------------------------------------------------------------------- #
    parser_export = subparsers.add_parser(
        name="export",
        add_help=True,
        help="""
            Export the records data to Stata.'
        """.replace(
            "\n", ""
        ),
    )

    parser_export.add_argument(
        "country",
        type=str,
        help="""Country to export.""".replace("\n", " "),
    )

    parser_export.set_defaults(func=parser_records_export)

    # ---------------------------------------------------------------------- #
    #                            Java Kill Parser                            #
    # ---------------------------------------------------------------------- #
    parser_java_kill = subparsers.add_parser(
        name="java-kill",
        add_help=True,
        help="""
            Terminate all processes associated with the scraping.'
        """.replace(
            "\n", ""
        ),
    )

    parser_java_kill.set_defaults(func=java_kill)

    # ---------------------------------------------------------------------- #
    #                              Scrape Parser                             #
    # ---------------------------------------------------------------------- #
    parser_scrape = subparsers.add_parser(
        name="scrape",
        add_help=True,
        help="""Start the main webscraping process.""".replace("\n", " "),
    )

    parser_scrape.add_argument(
        "country",
        type=str,
        nargs="?",
        default=get_prev_scraped_country(),
        help="""Country to scrape.""".replace("\n", " "),
    )

    parser_scrape.add_argument(
        "cent_start",
        type=int,
        nargs="?",
        default=1550,
        help="""Century to start scraping from.""".replace("\n", " "),
    )

    parser_scrape.add_argument(
        "cent_end",
        type=int,
        nargs="?",
        default=1890,
        help="""Century to scrape to.""".replace("\n", " "),
    )

    parser_scrape.add_argument(
        "--gui",
        action="store_false",
        default=True,
        dest="headless",
        help="""Start the Firefox browser with a
        Graphical User Interface (GUI).""".replace(
            "\n", " "
        ),
    )

    parser_scrape.set_defaults(func=scrape_main)

    return parser


def parse_main(args: Optional[list[str]] = None):
    """Command line function."""
    if args is None:
        args = sys.argv[1:]
    parser = main_parser()
    parsed_args = parser.parse_args()

    # Extract argument key values from parser
    args_key = vars(parsed_args)

    # Extract function from parser
    args_func: Callable[..., None] = args_key.pop("func", None)

    args_func(**args_key)
    return 0
