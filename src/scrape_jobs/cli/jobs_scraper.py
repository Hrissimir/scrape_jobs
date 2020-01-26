import argparse
import logging
import sys
from pathlib import Path
from tempfile import gettempdir

from hed_utils.support import log
from hed_utils.support.file_utils import get_stamp

from scrape_jobs import __version__, runner, config
from scrape_jobs.config import LOG_FORMAT

__author__ = "Hrissimir"
__copyright__ = "Hrissimir"
__license__ = "mit"

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(description="Scrape jobs and store results.")

    parser.add_argument("--version",
                        action="version",
                        version="scrape-jobs {ver}".format(ver=__version__))

    parser.add_argument("-v",
                        "--verbose",
                        dest="loglevel",
                        help="set loglevel to INFO",
                        action="store_const",
                        const=logging.INFO)

    parser.add_argument("-vv",
                        "--very-verbose",
                        dest="loglevel",
                        help="set loglevel to DEBUG",
                        action="store_const",
                        const=logging.DEBUG)

    default_file = str(Path.cwd().joinpath(config.CONFIG_FILENAME).absolute())
    parser.add_argument("-c",
                        dest="config_file",
                        action="store",
                        default=default_file,
                        type=str,
                        help=f"defaults to '{default_file}'")

    parser.add_argument(dest="site",
                        action="store",
                        choices={"seek.com.au", "linkedin.com"},
                        type=str,
                        help="site to scrape")

    return parser.parse_args(args)


def get_log_filepath() -> str:
    filename = "scrape-jobs_"
    filename += get_stamp()
    filename += ".log"
    return str(Path(gettempdir()).joinpath(filename).absolute())


def init_logging(level):
    logfile = get_log_filepath()
    log.init(level=level or logging.INFO, file=logfile, log_format=LOG_FORMAT)
    _log.info("initialized log-file at: %s", logfile)


def main(call_args):
    """Main entry point allowing external calls

    Args:
      call_args ([str]): command line parameter list
    """

    args = parse_args(call_args)
    init_logging(args.loglevel)

    _log.info("'scrape-jobs' called with args: %s", args)
    runner.run_with_config_file(args.site, args.config_file)


def run():
    """Entry point for 'scrape-jobs' CLI"""

    call_args = sys.argv[1:]
    main(call_args)
