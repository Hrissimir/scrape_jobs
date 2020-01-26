import argparse
import logging
import sys
from pathlib import Path
from tempfile import gettempdir

from hed_utils.support import log
from hed_utils.support.file_utils import get_stamp

from scrape_jobs import __version__, config

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def get_log_filepath() -> str:
    filename = "scrape-jobs-init-config_"
    filename += get_stamp()
    filename += ".log"
    return str(Path(gettempdir()).joinpath(filename).absolute())


def init_logging(level):
    logfile = get_log_filepath()
    log.init(level=level or logging.INFO, file=logfile, log_format=config.LOG_FORMAT)
    _log.info("initialized log-file at: %s", logfile)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(description="initialize sample 'scrape-jobs' config file")

    parser.add_argument("--version",
                        action="version",
                        version="scrape-jobs-init-config {ver}".format(ver=__version__))

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
    parser.add_argument("-f",
                        dest="file",
                        action="store",
                        default=default_file,
                        help=f"defaults to '{default_file}'")

    return parser.parse_args(args)


def init_config(file: str):
    contents = config.get_sample_contents()
    _log.debug("sample config contents:\n\n\n%s", contents.decode("utf-8"))

    filepath = Path(file).absolute()
    filepath.write_bytes(config.get_sample_contents())
    _log.info("created sample config at: '%s'", str(filepath))


def main(call_args):
    """Main entry point allowing external calls"""

    args = parse_args(call_args)
    init_logging(args.loglevel)
    _log.info("'scrape-jobs-init-config' called with args: %s", args)
    init_config(args.file)


def run():
    """Entry point for console_scripts"""

    call_args = sys.argv[1:]
    main(call_args)
