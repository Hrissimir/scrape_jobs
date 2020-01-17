from abc import ABC, abstractmethod
from operator import itemgetter
from pprint import pformat
from typing import NoReturn, List, Dict

from hed_utils.selenium import SharedDriver, chrome_driver
from hed_utils.support import log, time_tool

from scrape_jobs.common2.jobs_page import JobsPage
from scrape_jobs.common2.result_predicates import MaxDaysAge
from scrape_jobs.common2.scrape_config import ScrapeConfig


class JobsScraper(ABC):

    def __init__(self, config: ScrapeConfig, page: JobsPage):
        self.config = config
        self.page = page

    @abstractmethod
    def get_results_keys(self) -> List[str]:
        pass

    def scrape_raw_results_data(self) -> List[Dict[str, str]]:
        log.info("scraping raw results data begins...")

        log.info("navigating to jobs page...")
        page = self.page
        page.go_to(wait_for_url_changes=False, wait_for_page_load=True)

        search_params = self.config.get_search_params()
        log.info("setting search params: %s", search_params)
        page.set_search_params(**search_params)

        log.info("triggering a search and waiting for it to complete...")
        page.trigger_search()
        page.wait_for_search_complete()

        is_matching = MaxDaysAge(self.config.max_post_age_days)
        processed_results = []  # such that were met on another page
        matching_results = []  # those we'll return from this method
        is_first_time_no_unseen_matching = True

        while page.has_results():
            visible_results = [result.as_dict() for result in page.get_visible_results()]
            log.info("currently visible results: %s", len(visible_results))

            unseen_results = [result for result in visible_results if (result not in processed_results)]
            log.info("previously unseen results: %s", len(unseen_results))
            processed_results.extend(unseen_results)

            unseen_matching_results = [result for result in unseen_results if is_matching(result)]
            log.info("  unseen matching results: %s", len(unseen_matching_results))

            if unseen_matching_results:
                matching_results.extend(unseen_matching_results)
                is_first_time_no_unseen_matching = True
            else:
                log.warning("there were no new previously unseen results that match!")
                if is_first_time_no_unseen_matching:
                    log.warning("first time no matching results - will stop iteration next time")
                    is_first_time_no_unseen_matching = False
                else:
                    log.warning("second time no matching results - done iterating!")
                    break

            if page.has_next_page():
                log.info("Proceeding to next results page...")
                page.go_to_next_page()
                page.wait_for_search_complete()
            else:
                log.warning("No NEXT results page present - Done searching!")

        matching_results.sort(key=itemgetter("utc_datetime"))
        return matching_results

    def set_posted_timestamps(self, scraped_results: List[dict]) -> NoReturn:
        # convert the utc_datetime to date in target tz
        stamp_fmt = self.config.posted_timestamp_format
        tz_name = self.config.timezone or time_tool.get_local_tz_name()
        log.info("setting results posted timestamp fmt='%s', tz='%s'", stamp_fmt, tz_name)
        for result in scraped_results:
            utc_datetime = result.get("utc_datetime", None)
            if utc_datetime:
                tz_datetime = time_tool.utc_to_tz(utc_datetime, tz_name)
                result["utc_datetime"] = tz_datetime.strftime(stamp_fmt)

    def set_scraped_timestamps(self, rows: List[List[str]]) -> NoReturn:
        stamp_fmt = self.config.scraped_timestamp_format
        tz_name = self.config.timezone or time_tool.get_local_tz_name()
        log.info("pre-pending scrape timestamp with format '%s' (%s) to (%s) rows", stamp_fmt, tz_name, len(rows))
        utc_now = time_tool.utc_moment()
        tz_now = time_tool.utc_to_tz(utc_now, tz_name)
        stamp = tz_now.strftime(stamp_fmt)
        for row in rows:
            row.insert(0, stamp)

    def convert_to_rows(self, results_data: List[dict]) -> List[List[str]]:
        log.info("converting (%s) results data to rows...", len(results_data))
        rows = []
        for result in results_data:
            row = []

            for key in self.get_results_keys():
                value = result.get(key, None)
                row.append(str(value) if value else "N/A")

            rows.append(row)

        self.set_scraped_timestamps(rows)
        log.info("converted (%s) jobs to rows", len(rows))
        log.debug("got the following jobs rows:\n%s", pformat(rows, width=1000))
        return rows

    def scrape_jobs(self) -> List[List[str]]:
        log.info("scrape started with config: %s", self.config)

        log.info("starting chrome driver (headless=%s)", self.config.driver_headless)
        SharedDriver.set_driver(chrome_driver.create_instance(headless=self.config.driver_headless))
        try:
            raw_results = self.scrape_raw_results_data()
        except:
            log.exception("error while scraping raw results data")
            SharedDriver.get_instance().save_screenshot("scrape_error_screenshot.png")
            SharedDriver.get_instance().save_page_source("scrape_error_html.txt")
            raw_results = []
        finally:
            log.info("quitting chrome driver...")
            SharedDriver.get_instance().quit()
            SharedDriver.set_driver(None)

        log.info("scraped (%s) raw results", len(raw_results))
        self.set_posted_timestamps(raw_results)

        jobs = self.convert_to_rows(raw_results)
        return jobs
