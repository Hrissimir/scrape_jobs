# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from pathlib import Path

from hed_utils.support import log

from scrape_jobs import __version__
from scrape_jobs.common import scrape_config
from scrape_jobs.sites.linkedin_com import linkedin_scraper
from scrape_jobs.sites.seek_com_au import seek_scraper

__author__ = "Hrissimir"
__copyright__ = "Hrissimir"
__license__ = "mit"

SCRAPERS = {
    "seek.com.au": seek_scraper,
    "linkedin.com": linkedin_scraper
}


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


def scrape(site: str, config_file: str):
    site = site.strip().lower()
    config_path = Path(config_file.strip())
    SCRAPERS[site].start(str(config_path))


def init_config():
    file = Path.cwd().joinpath(scrape_config.SAMPLE_CONFIG_FILENAME)
    scrape_config.write_config(str(file))


def init_logging(level):
    level = level or logging.INFO
    log_file = Path.cwd().joinpath("scrape-jobs.log")

    if log_file.exists():
        try:
            log_file.unlink()
        except:
            pass

    log.init(level=level, file=str(log_file))


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    args = parse_args(args)
    init_logging(args.loglevel)

    log.info("Starting jobs scrape...")
    try:
        scrape(args.site, args.config_file)
    except:
        log.exception("error occurred while scraping!")
        exit(1)
    log.info("Jobs scrape complete!")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
