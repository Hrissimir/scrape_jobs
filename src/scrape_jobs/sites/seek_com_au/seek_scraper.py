import logging
from collections import namedtuple
from configparser import ConfigParser
from operator import itemgetter
from pathlib import Path
from pprint import pformat
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import google_spreadsheet
from hed_utils.support import log, time_tool

from scrape_jobs.common.result_predicates import MaxDaysAge
from scrape_jobs.common.scrape_config import Default, SeekComAu, read_config, assert_valid_config
from scrape_jobs.sites.seek_com_au.seek_page import SeekPage
from scrape_jobs.sites.seek_com_au.seek_result import SeekResult

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


def get_existing_urls(params: UploadParams) -> List[str]:
    spreadsheet = google_spreadsheet.connect(params.spreadsheet_name, params.json_auth_file)
    worksheet = spreadsheet.get_worksheet(params.worksheet_index)

    url_column_index = SeekResult.get_dict_keys().index("url") + 2  # not 0-based account for the prepended timestamp
    log.info("got url column index: %s", url_column_index)

    known_urls = worksheet.col_values(url_column_index)
    log.info("got (%s) pre-existing urls", len(known_urls))
    log.debug("known urls: \n%s", pformat(known_urls, width=1000))
    return known_urls


def scrape_raw_results(params: ScrapeParams) -> List[dict]:
    log.info("starting scrape with params: %s", params)

    results = []
    predicate = MaxDaysAge(params.days)

    driver.start_chrome()
    try:
        page = SeekPage()
        results.extend(page.search_and_collect(predicate, what=params.what, where=params.where))
    except:
        log.exception("error during scrape!")
        driver.save_screenshot("scrape_error.png")
        driver.save_source("scrape_error.html")
    finally:
        driver.quit()
        log.info("scrape returns %s raw results", len(results))
        results.sort(key=itemgetter("utc_datetime"))

    # convert the utc_datetime to date in target tz
    tz_name = params.tz or time_tool.get_local_tz_name()
    for result in results:
        utc_datetime = result.get("utc_datetime", None)
        if utc_datetime:
            tz_datetime = time_tool.utc_to_tz(utc_datetime, tz_name)
            result["utc_datetime"] = tz_datetime.strftime("%Y-%m-%d %H:%M")

    return results


def prepare_upload_rows(raw_results: List[dict], existing_urls: List[str]) -> List[List[str]]:
    log.info("preparing (%s) results for upload...")

    rows = []

    for result in raw_results:
        row = []

        url = result.get("url", None)

        if not url:
            continue

        if url in existing_urls:
            continue

        for key in SeekResult.get_dict_keys():
            value = result.get(key, None)
            row.append(str(value) if value else "N/A")

        rows.append(row)

    log.info("done - prepared (%s) rows for upload", len(rows))
    return rows


def upload_rows(rows_values: List[List[str]], params: UploadParams):
    log.info("starting results upload with params: %s...", params)

    spreadsheet = google_spreadsheet.connect(params.spreadsheet_name, params.json_auth_file)
    worksheet = spreadsheet.get_worksheet(params.worksheet_index)

    google_spreadsheet.append_rows_to_worksheet(rows_values, worksheet)


def prepend_scrape_timestamp(rows: List[List[str]], tz_name: str = None, fmt="%Y-%m-%d"):
    tz_name = tz_name or time_tool.get_local_tz_name()
    utcnow = time_tool.utc_moment()
    tznow = time_tool.utc_to_tz(utcnow, tz_name)
    stamp = tznow.strftime(fmt)
    for row in rows:
        row.insert(0, stamp)


def start(config_file: str):
    config = read_config(config_file)
    assert_valid_config(config)

    scrape_params = get_scrape_params(config)
    upload_params = get_upload_params(config)

    upload_error = google_spreadsheet.get_possible_append_row_error(spreadsheet_name=upload_params.spreadsheet_name,
                                                                    json_auth_file=upload_params.json_auth_file,
                                                                    worksheet_index=upload_params.worksheet_index,
                                                                    row_len=len(SeekResult.get_dict_keys()) + 1)
    if upload_error:
        raise RuntimeError(f"Won't be able to upload results! Reason: {upload_error}")

    results = scrape_raw_results(scrape_params)

    rows = prepare_upload_rows(results, get_existing_urls(upload_params))

    prepend_scrape_timestamp(rows, scrape_params.tz)

    upload_rows(rows, upload_params)


def main():
    config_path = Path("/home/re/PycharmProjects/scrape-jobs.ini")
    print(config_path)
    log.init(level=logging.INFO)
    start(str(config_path))


if __name__ == '__main__':
    main()
