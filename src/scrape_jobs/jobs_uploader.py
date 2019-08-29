from collections import namedtuple
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from hed_utils.support import google_spreadsheet, log

DATE_FMT = "%Y-%m-%d"

UploadParams = namedtuple("UploadParams",
                          ("jobs "
                           "spreadsheet_name "
                           "path_to_secrets_file "
                           "worksheet_index "
                           "worksheet_min_columns "
                           "worksheet_job_url_column_index"))


def get_upload_error(params: UploadParams) -> Optional[str]:
    secrets_path = Path(params.path_to_secrets_file)
    if not secrets_path.exists():
        return f"Upload secrets .json file is missing from '{secrets_path}'"

    try:
        spreadsheet = google_spreadsheet.connect(spreadsheet_name=params.spreadsheet_name,
                                                 path_to_secrets_file=params.path_to_secrets_file)
    except:
        return f"Could not open GoogleSpreadsheets document by name: [{params.spreadsheet_name}]"

    try:
        worksheet = spreadsheet.get_worksheet(params.worksheet_index)
    except:
        return f"Could not get worksheet with index: [{params.worksheet_index}] in [{params.spreadsheet_name}]"

    actual_worksheet_columns = worksheet.col_count
    if actual_worksheet_columns < params.worksheet_min_columns:
        return f"The worksheet # {params.worksheet_index} was expected to have " \
               f"at least [{params.worksheet_min_columns}] columns, but had only: [{actual_worksheet_columns}]"

    return None


def sort_jobs_by_date_asc(jobs: List[dict]):
    log.info("sorting jobs by date (asc) before upload...")

    def key(job: dict):
        return datetime.strptime(job["date"], DATE_FMT)

    jobs.sort(key=key)


def upload_jobs(params: UploadParams):
    log.info("uploading [ %s ] jobs with params: %s", len(params._replace(jobs=[])), params)

    sort_jobs_by_date_asc(params.jobs)

    try:
        log.info("opening GoogleSheets spreadsheet: %s", params.spreadsheet_name)
        spreadsheet = google_spreadsheet.connect(spreadsheet_name=params.spreadsheet_name,
                                                 path_to_secrets_file=params.path_to_secrets_file)
        try:
            log.info("opening worksheet #%s", params.worksheet_index)
            worksheet = spreadsheet.get_worksheet(params.worksheet_index)

            stored_jobs_urls = [url.strip()
                                for url
                                in worksheet.col_values(params.worksheet_job_url_column_index + 1)]  # 1-based columns

            log.info("there were %s pre-existing jobs in the sheet", len(stored_jobs_urls))
            from pprint import pformat
            log.info("pre-existing jobs urls: \n%s", pformat(stored_jobs_urls))

            new_jobs = [job
                        for job
                        in params.jobs
                        if (job["url"].strip() not in stored_jobs_urls)]

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
            log.exception("could not open worksheet #%s", params.worksheet_index)

        log.info("uploaded new jobs to sheet!")

    except:
        log.exception("could not connect to GoogleSheets!")
        raise

    log.info("done with jobs upload!")
