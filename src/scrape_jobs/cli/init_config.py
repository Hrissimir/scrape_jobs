import logging
from pathlib import Path

from hed_utils.support import log

from scrape_jobs.base import config

__author__ = "Hrissimir"
__copyright__ = "Hrissimir"
__license__ = "mit"

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

LOGFILE_NAME = "scrape-jobs-init-config.log"


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


def main():
    """Main entry point allowing external calls"""

    init_logging(logging.INFO)
    _log.info("'%s::main' called!", __file__)

    sample_contents = config.get_sample_contents()
    _log.info("got sample config contents:\n%s", sample_contents.decode("utf-8"))

    sample_filepath = Path.cwd().joinpath(config.CONFIG_FILENAME)
    _log.info("writing sample contents to: '%s'", str(sample_filepath))

    sample_filepath.write_bytes(sample_contents)
    _log.info("all done!")


def run():
    """Entry point for console_scripts"""

    main()


if __name__ == '__main__':
    main()
