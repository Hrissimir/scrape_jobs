import logging
from pathlib import Path
from tempfile import gettempdir
from time import perf_counter

from hed_utils.selenium import SharedDriver, chrome_driver

from scrape_jobs.base.data_collection import ACollector
from scrape_jobs.base.data_processing import TimeProcessor, AProcessor
from scrape_jobs.base.data_storage import AStorage, CsvJobsStorage, GoogleSheetsJobsStorage
from scrape_jobs.config import Config, SearchConfig, TimeConfig, SheetsConfig
from scrape_jobs.linkedin import LinkedinConfig, LinkedinJob, LinkedinPage
from scrape_jobs.program import Program
from scrape_jobs.seek import SeekConfig, SeekJob, SeekPage

CONFIG_CLASSES = {
    "linkedin.com": LinkedinConfig,
    "seek.com.au": SeekConfig
}

PAGE_CLASSES = {
    "linkedin.com": LinkedinPage,
    "seek.com.au": SeekPage
}

COLUMN_NAMES = {
    "linkedin.com": LinkedinJob.KEYS,
    "seek.com.au": SeekJob.KEYS
}

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def read_config(site: str, configfile: str) -> Config:
    configfile = str(Path(configfile).absolute())
    _log.info("Reading '%s' config from file: '%s'", site, configfile)

    try:
        clz = CONFIG_CLASSES[site]
    except KeyError as kerr:
        raise RuntimeError(f"Config not implemented for site: '{site}'!") from kerr

    try:
        return clz.parse_file(configfile)
    except Exception as err:
        raise RuntimeError(f"Error while reading config file!") from err


def init_driver(headless: bool):
    try:
        _log.info("Initializing driver... (headless: %s)", headless)
        driver = chrome_driver.create_instance(headless=headless)
    except Exception as err:
        raise RuntimeError("Could not create driver instance!") from err

    driver.set_page_load_timeout(10)
    SharedDriver.set_instance(driver)


def prepare_collector(site: str, search_cfg: SearchConfig) -> ACollector:
    _log.info("Preparing jobs collector with config: %s", search_cfg)

    init_driver(search_cfg.driver_headless)

    try:
        clz = PAGE_CLASSES[site]
    except KeyError as kerr:
        raise RuntimeError(f"Page not implemented for site: '{site}'!") from kerr

    try:
        return clz(search_cfg.search_params, search_cfg.max_post_age_days, search_cfg.max_attempts)
    except Exception as err:
        raise RuntimeError(f"Error during {clz.__name__} initialization!") from err


def prepare_processor(time_cfg: TimeConfig) -> AProcessor:
    _log.info("Preparing jobs processor with config: %s", time_cfg)
    try:
        return TimeProcessor(time_cfg.tz_name, time_cfg.scraped_fmt, time_cfg.posted_fmt)
    except Exception as err:
        raise RuntimeError("Error during jobs processor initialization!") from err


def get_csv_filepath(site: str) -> str:
    filename = site.replace(".", "_")
    filename += "_jobs"
    filename += ".csv"
    return str(Path(gettempdir()).joinpath(filename).absolute())


def prepare_storage(site: str, sheets_cfg: SheetsConfig) -> AStorage:
    _log.info("Preparing jobs storage with config: %s", sheets_cfg)
    try:
        columns = COLUMN_NAMES[site]
    except KeyError as kerr:
        raise RuntimeError(f"Storage column names not defined for site: '{site}'!") from kerr

    try:
        storage = GoogleSheetsJobsStorage(columns,
                                          sheets_cfg.spreadsheet_title,
                                          sheets_cfg.worksheet_title,
                                          sheets_cfg.json_filepath)
    except Exception as sheets_err:
        _log.warning("Error while initializing Google-Sheets storage! (%s) %s", type(sheets_err).__name__, sheets_err)

        try:
            filepath = get_csv_filepath(site)
            _log.warning("Using fallback storage CSV file: %s", filepath)
            storage = CsvJobsStorage(columns, filepath)
            if not storage.filepath.exists():
                storage.init_file()
        except Exception as csv_err:
            raise RuntimeError("Error while initializing CSV storage!") from csv_err

    return storage


def prepare_program(site: str, config: Config) -> Program:
    _log.info("Preparing program for execution...")
    try:
        collector = prepare_collector(site, config.search_config)
        processor = prepare_processor(config.time_config)
        storage = prepare_storage(site, config.sheets_config)
        return Program(collector, processor, storage)
    except Exception as err:
        raise RuntimeError("Error while creating program instance!") from err


def run_with_config(site: str, config: Config):
    program = prepare_program(site, config)
    try:
        _log.info("Starting program execution...")
        start_time = perf_counter()
        program.execute()
        end_time = perf_counter()
        took = end_time - start_time
        _log.info("Program execution completed! [took: %d min. %d s.]", took // 60, took % 60)
    except Exception as err:
        _log.exception("Error during program execution! ( %s ) %s", type(err).__name__, err)
        raise


def run_with_config_file(site: str, configfile: str):
    config = read_config(site, configfile)
    run_with_config(site, config)
