from collections import namedtuple
from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from hed_utils.selenium import driver
from hed_utils.support import log, time_tool, google_spreadsheet

from scrape_jobs.scrape_config import Default, SeekComAu, read_config, assert_valid_config
from scrape_jobs.sites.seek_com_au.seek_page import SeekPage, JobResult

DATE_FMT = "%Y-%m-%d"

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


def get_upload_error(params: UploadParams) -> Optional[str]:
    file = Path(params.file)
    if not file.exists():
        return f"Upload secrets .json file is missing from '{file}'"
    try:
        spreadsheet = google_spreadsheet.connect(spreadsheet_name=params.name, path_to_secrets_file=params.file)
    except:
        return f"Could not open GoogleSpreadsheets document by name: [{params.name}]"

    try:
        worksheet = spreadsheet.get_worksheet(params.sheet)
    except:
        return f"Could not get worksheet with index: [{params.sheet}]"

    expected_columns_count = len(JobResult.KEYS)
    actual_columns_count = worksheet.col_count
    if actual_columns_count < expected_columns_count:
        return f"The worksheet # {params.sheet} was expected to have " \
               f"at least [{expected_columns_count}] columns, but had only: [{actual_columns_count}]"

    return None


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


def upload_jobs(jobs: List[dict], params: UploadParams):
    log.info("uploading [ %s ] jobs with params: %s", len(jobs), params)

    try:
        log.info("opening GoogleSheets spreadsheet: %s", params.name)
        spreadsheet = google_spreadsheet.connect(spreadsheet_name=params.name, path_to_secrets_file=params.file)

        try:
            log.info("opening worksheet #%s", params.sheet)
            worksheet = spreadsheet.get_worksheet(params.sheet)
            job_url_column_idz = JobResult.KEYS.index("url")
            stored_jobs_urls = worksheet.col_values(job_url_column_idz)
            log.info("there were %s pre-existing jobs in the seet", len(stored_jobs_urls))
            new_jobs = [job
                        for job
                        in jobs
                        if job["url"] not in stored_jobs_urls]
            log.info("the scrape found %s new jobs", len(new_jobs))

            try:
                log.info("uploading new jobs to sheet...")
                for i, job in enumerate(new_jobs):
                    log.info("uploading job %s/%s ( %s )", i, len(new_jobs), job["title"])
                    values = list(job.values())
                    worksheet.append_row(values)
            except:
                log.exception("error while uploading new jobs to sheet!")
                raise

            log.info("done with new jobs upload!")

        except:
            log.exception("could not open worksheet #%s", params.sheet)

        log.info("uploaded new jobs to sheet!")

    except:
        log.exception("could not connect to GoogleSheets!")
        raise

    log.info("done with jobs upload!")


def sort_jobs_by_date_asc(jobs: List[dict]):
    log.info("sorting jobs by date (asc)...")

    def key(job: dict):
        return datetime.strptime(job["date"], DATE_FMT)

    jobs.sort(key=key)


def scrape(config_file: str):
    config = read_config(config_file)
    assert_valid_config(config)

    scrape_params = get_scrape_params(config)
    upload_params = get_upload_params(config)

    upload_error = get_upload_error(upload_params)
    if upload_error:
        raise RuntimeError(f"Jobs wont't be uploaded because [{upload_error}]!")

    jobs = scrape_jobs(scrape_params)
    sort_jobs_by_date_asc(jobs)
    upload_jobs(jobs, upload_params)
