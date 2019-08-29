# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = scrape_jobs.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import logging
import sys

from hed_utils.support import log

from scrape_jobs import __version__

__author__ = "Hrissimir"
__copyright__ = "Hrissimir"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(
        description="Perform jobs scrapping.")

    parser.add_argument(
        "--version",
        action="version",
        version="scrape_jobs {ver}".format(ver=__version__))

    parser.add_argument(
        dest="site",
        help="The target site / job-board name",
        type=str,
        metavar="SITE")

    parser.add_argument(
        dest="config_file",
        help="Path to .ini config file for the current execution",
        type=str,
        metavar="CONFIG_FILE")

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def scrape(site, config_file):
    pass


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    args = parse_args(args)
    log.init(args.loglevel)

    _logger.info("Starting jobs scrape...")
    scrape(args.site, args.config_file)
    _logger.info("Jobs scrape complete!")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
