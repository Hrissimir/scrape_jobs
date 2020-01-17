import pkgutil
from configparser import ConfigParser
from pathlib import Path
from typing import Optional, NoReturn

from hed_utils.support import log

FILENAME = "../common/scrape-jobs.ini"
CONTENTS = pkgutil.get_data("scrape_jobs.common", "scrape-jobs.ini").decode()


def get_config() -> ConfigParser:
    log.debug("sample config file contents:\n%s", CONTENTS)
    config = ConfigParser(interpolation=None)
    config.read_string(CONTENTS)
    return config


def write_to(file_path: Optional[str] = None) -> NoReturn:
    log.debug("writing sample config file at: '%s'", file_path)
    if not file_path:
        file_path = str(Path.cwd().joinpath(FILENAME))
        log.debug("deduced file path '%s'", file_path)

    with open(file_path, "wb") as configfile:
        configfile.write(CONTENTS.encode("utf-8"))