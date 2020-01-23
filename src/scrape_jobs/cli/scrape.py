import argparse
import logging
import sys
from pathlib import Path

from hed_utils.support import log

from scrape_jobs import __version__
from scrape_jobs.base import Program

__author__ = "Hrissimir"
__copyright__ = "Hrissimir"
__license__ = "mit"

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

LOGFILE_NAME = "scrape-jobs.log"


def init_logging(level):
    level = level or logging.INFO
    filepath = Path.cwd().joinpath(LOGFILE_NAME)

    if filepath.exists():
        try:
            filepath.unlink()
        except:  # pragma: no cover
            pass
    fmt = log.LOG_FORMAT.replace("%(name)s | ", "")
    log.init(level=level, file=str(filepath), log_format=fmt)


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
        "-s",
        "--site",
        dest="site",
        action="store",
        choices={"seek.com.au", "linkedin.com"},
        help="target site")

    parser.add_argument(
        "-c",
        "--cfg",
        dest="config_file",
        action="store",
        help="path to config.ini file")

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


def main(call_args):
    """Main entry point allowing external calls

    Args:
      call_args ([str]): command line parameter list
    """

    _log.info("'scrape-jobs.py::main' called with args: %s", call_args)

    args = parse_args(call_args)
    _log.debug("parsed args: %s", args)

    init_logging(args.loglevel)

    program = None
    try:
        program = Program.init(args.site, args.config_file)
    except Exception as init_error:  # pragma: no cover
        _log.exception("error during program initialization! ( %s ) %s", type(init_error).__name__, init_error)
        exit(1)

    try:
        program.start()
    except Exception as exec_error:
        _log.exception("error during program execution! ( %s ) %s", type(exec_error).__name__, exec_error)
        exit(1)

    _log.info("Jobs scrape complete!")


def run():
    """Entry point for 'scrape-jobs' CLI"""

    call_args = sys.argv[1:]
    main(call_args)
