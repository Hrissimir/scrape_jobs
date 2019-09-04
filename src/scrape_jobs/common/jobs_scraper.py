from abc import ABC, abstractmethod, abstractclassmethod
from configparser import ConfigParser
from typing import NoReturn, List, Dict

from hed_utils.selenium import driver
from hed_utils.support import log, google_spreadsheet, time_tool

from scrape_jobs.common.scrape_config import read_config, assert_valid_config


class Params(ABC):

    @abstractclassmethod
    def parse(cls, config: ConfigParser):
        pass


class ScrapeParams(Params, ABC):
    def __init__(self, tz: str):
        self.tz = tz


class UploadParams(Params, ABC):
    def __init__(self, spreadsheet_name: str, json_auth_file: str, worksheet_index: int):
        self.spreadsheet_name = spreadsheet_name
        self.json_auth_file = json_auth_file
        self.worksheet_index = worksheet_index


class JobsScraper(ABC):

    def __init__(self, config_file):
        self.config = self.read_config(config_file)

    @classmethod
    def read_config(cls, config_file) -> ConfigParser:
        config = read_config(config_file)
        assert_valid_config(config)
        return config

    @abstractmethod
    def get_scrape_params(self) -> ScrapeParams:
        pass

    @abstractmethod
    def get_upload_params(self) -> UploadParams:
        pass

    @abstractmethod
    def check_for_upload_errors(self) -> NoReturn:
        pass

    @abstractmethod
    def get_existing_jobs_urls(self) -> List[str]:
        pass

    @abstractmethod
    def scrape_raw_results_data(self, params: ScrapeParams) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def prepare_rows_for_upload(self, raw_results: List[dict]) -> List[List[str]]:
        pass

    @classmethod
    def prepend_scrape_timestamp(cls,
                                 rows: List[List[str]],
                                 tz_name: str = None,
                                 fmt="%Y-%m-%d"):
        log.info("pre-pending scrape timestamp with format '%s' to (%s) rows", fmt, len(rows))
        tz_name = tz_name or time_tool.get_local_tz_name()
        utcnow = time_tool.utc_moment()
        tznow = time_tool.utc_to_tz(utcnow, tz_name)
        stamp = tznow.strftime(fmt)
        for row in rows:
            row.insert(0, stamp)

    @classmethod
    def upload_rows(self, rows: List[List[str]], params: UploadParams):
        if not rows:
            log.warning("No rows (%s) were present for upload! Params: %s", rows, params)
            return

        log.info("starting upload of (%s) rows with params: %s...", len(rows), params)
        spreadsheet = google_spreadsheet.connect(params.spreadsheet_name, params.json_auth_file)
        worksheet = spreadsheet.get_worksheet(params.worksheet_index)
        google_spreadsheet.append_rows_to_worksheet(rows, worksheet)
        log.info("done uploading (%s) rows", len(rows))

    def filter_new_results(self, raw_results: List[dict]) -> List[dict]:
        log.info("filtering new results out of '%s' raw results", len(raw_results))
        if not raw_results:
            log.warning("no raw results to filter! (%s)", raw_results)
            return []

        existing_urls = self.get_existing_jobs_urls()
        log.info("got (%s) pre-existing records", len(existing_urls))
        new_results = [result
                       for result
                       in raw_results
                       if result["url"] not in existing_urls]
        log.info("got (%s) new results for upload", len(new_results))
        return new_results

    def start(self):
        self.check_for_upload_errors()

        scrape_params = self.get_scrape_params()
        log.info("got scrape params: %s", scrape_params)

        driver.start_chrome()
        try:
            raw_results_data = self.scrape_raw_results_data(scrape_params)
        except:
            log.exception("error while scraping raw results")
            driver.save_screenshot("scrape_error_screenshot.png")
            driver.save_source("scrape_error_html.txt")
            raw_results_data = []
        finally:
            driver.quit()

        log.info("got (%s) raw results", len(raw_results_data))

        new_results_data = self.filter_new_results(raw_results_data)

        rows_for_upload = self.prepare_rows_for_upload(new_results_data)
        log.info("prepared (%s) rows for upload", len(rows_for_upload))

        self.prepend_scrape_timestamp(rows_for_upload, scrape_params.tz)
        upload_params = self.get_upload_params()

        self.upload_rows(rows_for_upload, upload_params)
