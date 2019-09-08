from pprint import pformat
from typing import NoReturn, List

from hed_utils.support import log, google_spreadsheet

from scrape_jobs.common.upload_config import UploadConfig


class JobsUploader:
    def __init__(self, config: UploadConfig):
        self.config = config

    def check_for_upload_errors(self) -> NoReturn:
        details = dict(spreadsheet_name=self.config.upload_spreadsheet_name,
                       json_auth_file=self.config.upload_spreadsheet_json,
                       worksheet_index=self.config.upload_worksheet_index,
                       row_len=self.config.upload_worksheet_expected_columns_count)
        log.info("checking for possible upload errors using details: %s", details)
        error = google_spreadsheet.get_possible_append_row_error(**details)
        if error:
            raise RuntimeError(f"Error will occur upon upload: '{error}'")
        log.info("found no possible upload errors")

    def open_worksheet(self):
        spreadsheet_name = self.config.upload_spreadsheet_name
        json_auth_file = self.config.upload_spreadsheet_json
        worksheet_index = self.config.upload_worksheet_index
        params = dict(spreadsheet_name=spreadsheet_name,
                      json_auth_file=json_auth_file,
                      worksheet_index=worksheet_index)
        log.info("opening worksheet with params: %s...", params)
        spreadsheet = google_spreadsheet.connect(spreadsheet_name, json_auth_file)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        return worksheet

    def get_known_jobs_urls(self) -> List[str]:
        col_idx = self.config.upload_worksheet_urls_column_index
        log.info("retrieving pre-existing jobs urls from column # : %s", col_idx)

        worksheet = self.open_worksheet()
        urls = worksheet.col_values(col_idx)
        log.info("there were (%s) pre-existing job urls in the worksheet", len(urls))

        log.debug("pre-existing job urls: \n%s", pformat(urls, width=1000))
        return urls[1:]  # skip the first as it's the column name

    def get_new_jobs(self, scraped_jobs: List[List[str]]) -> List[List[str]]:
        log.info("getting new jobs out of '%s' scraped jobs", len(scraped_jobs))
        if not scraped_jobs:
            log.warning("no scraped jobs present! (%s)", scraped_jobs)
            return []

        known_urls = self.get_known_jobs_urls()
        url_idx = self.config.upload_worksheet_urls_column_index - 1

        new_jobs = [result
                    for result
                    in scraped_jobs
                    if result[url_idx] not in known_urls]
        log.info("got [ %s ] new jobs out of [ %s ] scraped jobs", len(new_jobs), len(scraped_jobs))
        return new_jobs

    def upload_jobs(self, scraped_jobs: List[List[str]]) -> NoReturn:
        if not scraped_jobs:
            log.warning("No jobs (%s) were present for upload!", scraped_jobs)
            return

        new_jobs = self.get_new_jobs(scraped_jobs)
        log.info("uploading (%s) new jobs to worksheet...", len(new_jobs))

        worksheet = self.open_worksheet()
        google_spreadsheet.append_rows_to_worksheet(new_jobs, worksheet)

        log.info("done uploading (%s) new jobs", len(new_jobs))
