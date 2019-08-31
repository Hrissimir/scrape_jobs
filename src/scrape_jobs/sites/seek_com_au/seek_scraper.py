from collections import namedtuple
from configparser import ConfigParser
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import google_spreadsheet
from hed_utils.support import log

from scrape_jobs.common import jobpost
from scrape_jobs.common.jobs_page import search_and_collect
from scrape_jobs.scrape_config import Default, SeekComAu, read_config, assert_valid_config
from scrape_jobs.sites.seek_com_au import seek_job
from scrape_jobs.sites.seek_com_au.seek_page import SeekPage

ScrapeParams = namedtuple("ScrapeParams", "what where days tz")
UploadParams = namedtuple("UploadParams", "spreadsheet_name json_auth_file worksheet_index")


def get_scrape_params(config: ConfigParser) -> ScrapeParams:
    what = config.get(SeekComAu.KEY, SeekComAu.WHAT)
    where = config.get(SeekComAu.KEY, SeekComAu.WHERE)
    days = config.getint(SeekComAu.KEY, SeekComAu.DAYS)
    tz = config.get(SeekComAu.KEY, SeekComAu.TIMEZONE)
    scrape_params = ScrapeParams(what, where, days, tz)
    log.info("parsed scrape params: %s", scrape_params)
    return scrape_params


def get_upload_params(config: ConfigParser) -> UploadParams:
    spreadsheet_name = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_NAME)
    secrets_json = config.get(Default.KEY, Default.UPLOAD_SPREADSHEET_JSON)
    worksheet_idx = config.getint(SeekComAu.KEY, SeekComAu.UPLOAD_WORKSHEET_INDEX)

    params = UploadParams(spreadsheet_name, secrets_json, worksheet_idx)
    log.info("parsed upload params from config: %s", params)
    return params


def scrape_raw_results(params: ScrapeParams) -> List[dict]:
    log.info("starting scrape with params: %s", params)

    results = []
    predicate = jobpost.age_predicate(n_days=params.days, tz_name=params.tz)

    driver.start_chrome()
    try:
        for result in search_and_collect(SeekPage(), predicate, what=params.what, where=params.where):
            result_posted = jobpost.get_date(result)
            result_date = jobpost.parse_posted_datetime(result_posted, params.tz).date()
            jobpost.set_date(result, result_date.strftime("%Y-%m-%d"))
            results.append(result)
    except:
        log.exception("error during scrape!")
        driver.save_screenshot("scrape_error.png")
        driver.save_source("scrape_error.html")
    finally:
        driver.quit()
        log.info("scrape returns %s raw results", len(results))
        results.sort(key=jobpost.get_date)
        return results


def prepare_upload_rows(raw_results: List[dict]) -> List[List[str]]:
    log.info("preparing (%s) results for upload...")

    rows = []
    for result in raw_results:
        row = [str(result[key]) for key in seek_job.KEYS]
        rows.append(row)

    log.info("done - prepared (%s) rows for upload", len(rows))
    return rows


def upload_results(rows_values: List[List[str]], params: UploadParams):
    log.info("starting results upload with params: %s...", params)

    spreadsheet = google_spreadsheet.connect(params.spreadsheet_name, params.json_auth_file)
    worksheet = spreadsheet.get_worksheet(params.worksheet_index)

    # filter pre-existing results
    url_key_idx = seek_job.KEYS.index("url")
    known_urls = worksheet.col_values(url_key_idx)
    log.info("...the worksheet already had %s records", len(known_urls))
    unseen_rows = [row for row in rows_values if not (row[url_key_idx] in known_urls)]
    log.info("*** uploading '%s' unseen rows (out of %s scraped) *** ... ", len(unseen_rows), len(rows_values))

    google_spreadsheet.append_rows_to_worksheet(unseen_rows, worksheet)


def start(config_file: str):
    config = read_config(config_file)
    assert_valid_config(config)

    scrape_params = get_scrape_params(config)
    upload_params = get_upload_params(config)

    upload_error = google_spreadsheet.get_possible_append_row_error(spreadsheet_name=upload_params.spreadsheet_name,
                                                                    json_auth_file=upload_params.json_auth_file,
                                                                    worksheet_index=upload_params.worksheet_index,
                                                                    row_len=len(seek_job.KEYS))
    if upload_error:
        raise RuntimeError(f"Won't be able to upload results! Reason: {upload_error}")

    raw_results = scrape_raw_results(scrape_params)

    rows_values = prepare_upload_rows(raw_results)

    upload_results(rows_values, upload_params)
