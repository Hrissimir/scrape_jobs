from collections import namedtuple
from configparser import ConfigParser
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log

from scrape_jobs import jobs_uploader
from scrape_jobs.jobs_uploader import UploadParams
from scrape_jobs.scrape_config import Default, SeekComAu, read_config, assert_valid_config
from scrape_jobs.sites.seek_com_au.seek_job_result import SeekJobResult
from scrape_jobs.sites.seek_com_au.seek_jobs_page import SeekJobsPage

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
    job_keys = SeekJobResult.get_dict_keys()
    min_columns = len(job_keys)
    job_url_col_idx = job_keys.index("url")
    return UploadParams(jobs, spreadsheet_name, secrets_json, worksheet_idx, min_columns, job_url_col_idx)


def scrape_jobs(params: ScrapeParams) -> List[dict]:
    log.debug("scraping jobs with params: %s", params)

    jobs = []

    driver.start_chrome()
    try:
        page = SeekJobsPage()
        page.go_to()
        jobs.extend(page.collect_most_recent_jobs(params.what, params.where, params.days, params.tz))
    except:
        log.exception("error while scraping jobs!")
        driver.save_screenshot("scrape_error.png")
    finally:
        driver.quit()
        log.debug("done scraping jobs - got %s matching jobs!", len(jobs))
        return jobs


def scrape(config_file: str):
    """Expected sheet columns:
        ['date', 'location', 'title', 'company', 'classification', 'url', 'is_featured', 'salary']
    """

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
