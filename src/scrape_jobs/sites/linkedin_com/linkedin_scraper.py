import logging
from configparser import ConfigParser
from operator import itemgetter
from pathlib import Path
from pprint import pformat
from typing import List, Dict, NoReturn

from hed_utils.selenium import driver
from hed_utils.support import google_spreadsheet
from hed_utils.support import log, time_tool

from scrape_jobs.common.jobs_scraper import ScrapeParams, UploadParams, JobsScraper
from scrape_jobs.common.result_predicates import MaxDaysAge
from scrape_jobs.common.scrape_config import Default, LinkedinCom
from scrape_jobs.sites.linkedin_com.linkedin_job_result import LinkedinJobResult
from scrape_jobs.sites.linkedin_com.linkedin_jobs_page import LinkedinJobsPage
from scrape_jobs.sites.linkedin_com.linkedin_search_filters import DatePostedFilter


class LinkedinScrapeParams(ScrapeParams):
    def __init__(self, keywords: str, location: str, date_posted: str, days: int, tz: str):
        super().__init__(tz)
        self.keywords = keywords
        self.location = location
        self.date_posted = date_posted
        self.days = days

    def __repr__(self):
        return f"LinkedinScrapeParams(" \
               f"keywords='{self.keywords}', " \
               f"location='{self.location}', " \
               f"date_posted='{self.date_posted}', " \
               f"days={self.days}, " \
               f"tz='{self.tz}')"

    @classmethod
    def parse(cls, config: ConfigParser):
        log.info("parsing upload params...")
        cfg = config[LinkedinCom.KEY]
        keywords = cfg.get(LinkedinCom.KEYWORDS)
        location = cfg.get(LinkedinCom.LOCATION)
        date_posted = cfg.get(LinkedinCom.DATE_POSTED, fallback=DatePostedFilter.PAST_MONTH)
        days = cfg.getint(LinkedinCom.DAYS)
        tz = cfg.get(LinkedinCom.TIMEZONE)
        return cls(keywords, location, date_posted, days, tz)


class LinkedinUploadParams(UploadParams):
    def __repr__(self):
        return f"{type(self).__name__}(" \
               f"spreadsheet_name='{self.spreadsheet_name}', " \
               f"json_auth_file='{self.json_auth_file}', " \
               f"worksheet_index={self.worksheet_index})"

    @classmethod
    def parse(cls, config: ConfigParser):
        log.info("parsing scrape params...")
        spreadsheet_name = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_NAME)
        secrets_json = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_JSON)
        worksheet_idx = config.getint(LinkedinCom.KEY, LinkedinCom.UPLOAD_WORKSHEET_INDEX)
        return cls(spreadsheet_name, secrets_json, worksheet_idx)


class LinkedinJobsScraper(JobsScraper):

    @classmethod
    def get_page(cls) -> LinkedinJobsPage:
        log.info("creating page object...")
        return LinkedinJobsPage()

    def get_scrape_params(self) -> LinkedinScrapeParams:
        return LinkedinScrapeParams.parse(self.config)

    def get_upload_params(self) -> LinkedinUploadParams:
        return LinkedinUploadParams.parse(self.config)

    def check_for_upload_errors(self) -> NoReturn:
        log.info("checking for possible upload errors...")
        upload_params = self.get_upload_params()
        upload_error = google_spreadsheet.get_possible_append_row_error(
            spreadsheet_name=upload_params.spreadsheet_name,
            json_auth_file=upload_params.json_auth_file,
            worksheet_index=upload_params.worksheet_index,
            row_len=len(LinkedinJobResult.get_dict_keys()) + 1)

        if upload_error:
            raise RuntimeError(f"Won't be able to upload results! Reason: {upload_error}")
        else:
            log.info("no upload errors should be present!")

    def get_known_jobs_urls(self) -> List[str]:
        params = self.get_upload_params()
        spreadsheet = google_spreadsheet.connect(params.spreadsheet_name, params.json_auth_file)
        worksheet = spreadsheet.get_worksheet(params.worksheet_index)

        url_key_idx = LinkedinJobResult.get_dict_keys().index("url") + 2
        log.info("got url column index: %s", url_key_idx)

        known_urls = worksheet.col_values(url_key_idx)
        log.info("got %s known urls", len(known_urls))
        log.debug("known urls: \n%s", pformat(known_urls, width=1000))
        return known_urls

    def scrape_raw_results_data(self, params: LinkedinScrapeParams) -> List[Dict[str, str]]:
        results = []
        predicate = MaxDaysAge(params.days)

        try:
            page = LinkedinJobsPage()
            results.extend(page.search_and_collect(predicate,
                                                   keywords=params.keywords,
                                                   location=params.location,
                                                   date_posted=params.date_posted))
        except Exception as err:
            log.exception("error during linkedin scrape! (%s)", err)
            driver.save_screenshot("linkedin_scrape_error_screenshot.png")
            driver.save_source("linkedin_scrape_error_html.txt")
        finally:
            log.info("scrape got (%s) raw results", len(results))
            results.sort(key=itemgetter("utc_datetime"))

        # convert the utc_datetime to date in target tz
        tz_name = params.tz or time_tool.get_local_tz_name()
        for result in results:
            utc_datetime = result.get("utc_datetime", None)
            if utc_datetime:
                tz_datetime = time_tool.utc_to_tz(utc_datetime, tz_name)
                result["utc_datetime"] = tz_datetime.strftime("%Y-%m-%d")

        return results

    def convert_to_rows(self, results_data: List[dict]) -> List[List[str]]:
        log.info("preparing (%s) results for upload...", len(results_data))
        rows = []
        for result in results_data:
            row = []

            for key in LinkedinJobResult.get_dict_keys():
                value = result.get(key, None)
                row.append(str(value) if value else "N/A")

            rows.append(row)

        log.info("done - prepared (%s) rows for upload", len(rows))
        log.debug("prepared rows for upload:\n%s", pformat(rows, width=1000))
        return rows


def start(config_file: str):
    scraper = LinkedinJobsScraper(config_file)
    scraper.start()


def main():
    config_path = Path("/home/re/PycharmProjects/scrape-jobs.ini")
    print(config_path)
    log.init(level=logging.INFO)
    scraper = LinkedinJobsScraper(str(config_path))
    scraper.start()


if __name__ == '__main__':
    main()
