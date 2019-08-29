from collections import namedtuple
from configparser import ConfigParser
from datetime import datetime, timedelta
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log, time_tool

from scrape_jobs import jobs_uploader
from scrape_jobs.jobs_uploader import UploadParams, sort_jobs_by_date_asc
from scrape_jobs.scrape_config import Default, SeekComAu, read_config, assert_valid_config
from scrape_jobs.sites.seek_com_au.seek_page import SeekPage, JobResult

DATE_FMT = "%Y-%m-%d"

ScrapeParams = namedtuple("ScrapeParams", "what where days tz")


def get_scrape_params(config: ConfigParser) -> ScrapeParams:
    what = config.get(SeekComAu.KEY, SeekComAu.WHAT)
    where = config.get(SeekComAu.KEY, SeekComAu.WHERE)
    days = config.getint(SeekComAu.KEY, SeekComAu.DAYS)
    tz = config.get(SeekComAu.KEY, SeekComAu.TIMEZONE)
    scrape_params = ScrapeParams(what, where, days, tz)
    log.debug("got scrape params: %s", scrape_params)
    return scrape_params


def get_default_upload_params(config: ConfigParser) -> UploadParams:
    jobs = []
    spreadsheet_name = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_NAME)
    secrets_json = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_JSON)
    worksheet_idx = config.getint(SeekComAu.KEY, SeekComAu.UPLOAD_WORKSHEET_INDEX)
    min_columns = len(JobResult.KEYS)
    job_url_col_idx = JobResult.KEYS.index("url")
    return UploadParams(jobs, spreadsheet_name, secrets_json, worksheet_idx, min_columns, job_url_col_idx)


def get_stop_date(days, tz) -> str:
    tz_datetime = time_tool.convert_to_tz(datetime.now(), tz)
    stop_date = str((tz_datetime - timedelta(days=days)).date())
    log.debug("got seek.com.au stop date: '%s'", stop_date)
    return stop_date


def perform_search(what, where) -> SeekPage:
    page = SeekPage()
    page.go_to()
    page.set_search_keywords(what)
    page.set_search_location(where)
    page.trigger_search()
    page.wait_for_search_results()
    page.set_sort_by("Date")
    page.wait_for_search_results()
    log.info("Total job results count: %s", page.get_total_jobs_found())
    return page


def get_visible_matching_jobs(page: SeekPage, days: int, tz: str):
    stop_date = get_stop_date(days, tz)
    stop_datetime = datetime.strptime(stop_date, DATE_FMT)

    def is_bad_date(date: str) -> bool:
        try:
            return datetime.strptime(date, DATE_FMT) <= stop_datetime
        except ValueError:
            return True

    return [job
            for job
            in page.get_visible_results_data(tz)
            if not is_bad_date(job["date"])]


def scrape_jobs(params: ScrapeParams) -> List[dict]:
    log.debug("scraping jobs with params: %s", params)

    jobs = []

    driver.start_chrome()
    try:
        page = perform_search(params.what, params.where)

        page_num = 1
        is_first_bad_page = True
        while True:
            log.info("processing results page #%s", page_num)

            matching_jobs = get_visible_matching_jobs(page, params.days, params.tz)
            if not matching_jobs:
                if is_first_bad_page:
                    log.info("current page did not contain matching jobs - will stop the search on next occurrence")
                    is_first_bad_page = False
                    page_num += 1
                    continue
                else:
                    log.info("current page was second page in a row with no matching results - search completed!")
                    break

            log.info("got %s matching jobs from current page!", len(matching_jobs))
            jobs.extend(matching_jobs)
            page.go_to_next_page()
            page.wait_for_search_results()
            page_num += 1

    except:
        log.exception("error while scraping jobs!")
        driver.save_screenshot("scrape_error.png")
    finally:
        driver.quit()
        log.debug("done scraping jobs - got %s matching jobs!", len(jobs))
        return jobs


def scrape(config_file: str):
    config = read_config(config_file)
    assert_valid_config(config)

    scrape_params = get_scrape_params(config)
    default_upload_params = get_default_upload_params(config)

    upload_error = jobs_uploader.get_upload_error(default_upload_params)
    if upload_error:
        raise RuntimeError(f"Jobs wont't be uploaded because [{upload_error}]!")

    jobs = scrape_jobs(scrape_params)
    upload_params = default_upload_params._replace(jobs=jobs)
    jobs_uploader.upload_jobs(upload_params)
