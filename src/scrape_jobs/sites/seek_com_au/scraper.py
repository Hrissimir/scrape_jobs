from collections import namedtuple
from configparser import ConfigParser
from pathlib import Path

from hed_utils.support import log

from scrape_jobs.scrape_config import Default, SeekComAu, read_config, assert_valid_config

ScrapeParams = namedtuple("ScrapeParams", "what where days tz")
UploadParams = namedtuple("UploadParams", "name file sheet")


def get_scrape_params(config: ConfigParser) -> ScrapeParams:
    what = config.get(SeekComAu.KEY, SeekComAu.WHAT)
    where = config.get(SeekComAu.KEY, SeekComAu.WHERE)
    days = config.getint(SeekComAu.KEY, SeekComAu.DAYS)
    tz = config.get(SeekComAu.KEY, SeekComAu.TIMEZONE)
    scrape_params = ScrapeParams(what, where, days, tz)
    log.debug("got scrape params: %s", scrape_params)
    return scrape_params


def get_upload_params(config: ConfigParser) -> UploadParams:
    name = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_NAME)
    file = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_JSON)
    sheet = config.getint(SeekComAu.KEY, SeekComAu.UPLOAD_WORKSHEET_INDEX)
    upload_params = UploadParams(name, file, sheet)
    log.debug("got upload params: %s", upload_params)
    return upload_params


def assert_upload_params(params: UploadParams):
    file = Path(params.file)
    assert file.exists(), f"upload secrets .json file is missing from '{file}'"


def scrape(config_file: str):
    config = read_config(config_file)
    assert_valid_config(config)
    scrape_params = get_scrape_params(config)
    upload_params = get_upload_params(config)
    assert_upload_params(upload_params)
