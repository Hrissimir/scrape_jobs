import os
from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import MagicMock, patch

from hed_utils.support import google_spreadsheet

from scrape_jobs.common.jobs_uploader import JobsUploader
# Config targeting a test Worksheet in the actual Spreadsheet
from scrape_jobs.common.upload_config import UploadConfig

DEFAULT_CONFIG_DICT = {
    "DEFAULT":
        {
            "upload_spreadsheet_name": "jobs_stats_data",
            "upload_spreadsheet_json": os.environ["JOBS_AUTH_FILE"],
            "upload_worksheet_index": 2,
            "upload_worksheet_expected_columns_count": 6,
            "upload_worksheet_urls_column_index": 6
        }
}

KNOWN_URLS = [
    "https://bg.linkedin.com/jobs/view/test-automation-engineer-at-fadata-group-1442742119",
    "https://bg.linkedin.com/jobs/view/mid-level-automation-qa-engineer-at-astrea-recruitment-1445492054",
    "https://bg.linkedin.com/jobs/view/automation-qa-web-apis-services-at-jtr-1445043922",
    "https://bg.linkedin.com/jobs/view/senior-automation-qa-web-apis-services-at-jtr-1445066435"
]


def create_default_uploader() -> JobsUploader:
    config = ConfigParser()
    config.read_dict(DEFAULT_CONFIG_DICT)

    upload_config = UploadConfig("DEFAULT", config)
    uploader = JobsUploader(upload_config)

    return uploader


class TestJobsUploader(TestCase):

    def test_check_for_upload_errors_no_errors(self):
        uploader = create_default_uploader()
        mock_check_method = MagicMock()
        mock_check_method.return_value = None

        with patch.object(google_spreadsheet, "get_possible_append_row_error", mock_check_method):
            uploader.check_for_upload_errors()

        mock_check_method.assert_called_once_with(
            spreadsheet_name=uploader.config.upload_spreadsheet_name,
            json_auth_file=uploader.config.upload_spreadsheet_json,
            worksheet_index=uploader.config.upload_worksheet_index,
            row_len=uploader.config.upload_worksheet_expected_columns_count
        )

    def test_check_for_upload_errors_with_errors(self):
        uploader = create_default_uploader()

        mock_check = MagicMock()
        mock_check.return_value = ["Error Message"]
        with patch.object(google_spreadsheet, "get_possible_append_row_error", mock_check):
            with self.assertRaises(RuntimeError, msg="Error will occur upon upload: 'Error Message'"):
                uploader.check_for_upload_errors()

        mock_check.assert_called_once_with(
            spreadsheet_name=uploader.config.upload_spreadsheet_name,
            json_auth_file=uploader.config.upload_spreadsheet_json,
            worksheet_index=uploader.config.upload_worksheet_index,
            row_len=uploader.config.upload_worksheet_expected_columns_count)

    def test_open_worksheet(self):
        uploader = create_default_uploader()

        mock_spreadsheet = MagicMock()
        mock_connect = MagicMock()
        mock_connect.return_value = mock_spreadsheet
        mock_worksheet = object()
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet

        with patch.object(google_spreadsheet, "connect", mock_connect):
            worksheet = uploader.open_worksheet()

        mock_connect.assert_called_once_with(
            uploader.config.upload_spreadsheet_name,
            uploader.config.upload_spreadsheet_json,
        )

        mock_spreadsheet.get_worksheet.assert_called_once_with(uploader.config.upload_worksheet_index)

        self.assertIs(mock_worksheet, worksheet)

    def test_get_known_jobs_urls_real_workflow(self):
        uploader = create_default_uploader()
        actual_urls = uploader.get_known_jobs_urls()
        self.assertListEqual(KNOWN_URLS, actual_urls)

    def test_get_new_jobs_from_list_with_jobs(self):
        uploader = create_default_uploader()
        new_job = ["scraped", "posted", "location", "title", "company", "url"]
        all_jobs = [
            ["", "", "", "", "", "https://bg.linkedin.com/jobs/view/automation-qa-web-apis-services-at-jtr-1445043922"],
            new_job
        ]
        expected_new_jobs = [new_job]

        mock_get_urls = MagicMock()
        mock_get_urls.return_value = KNOWN_URLS
        with patch.object(uploader, "get_known_jobs_urls", mock_get_urls):
            actual_new_jobs = uploader.get_new_jobs(all_jobs)
            self.assertListEqual(expected_new_jobs, actual_new_jobs)

    def test_get_new_jobs_from_list_with_no_jobs(self):
        uploader = create_default_uploader()

        mock_get_known_jobs_urls = MagicMock()
        expected_jobs = []

        with patch.object(uploader, "get_known_jobs_urls", mock_get_known_jobs_urls):
            actual_jobs = uploader.get_new_jobs([])

        mock_get_known_jobs_urls.assert_not_called()
        self.assertListEqual(expected_jobs, actual_jobs)

    def test_upload_jobs(self):
        uploader = create_default_uploader()

        a_job = ["scraped", "posted", "location", "title", "company", "url"]
        jobs_for_upload = [a_job]

        mock_get_new_jobs = MagicMock()
        mock_get_new_jobs.return_value = jobs_for_upload

        mock_open_worksheet = MagicMock()
        mock_worksheet = object()
        mock_open_worksheet.return_value = mock_worksheet

        mock_append_rows = MagicMock()

        with patch.object(uploader, "get_new_jobs", mock_get_new_jobs):
            with patch.object(uploader, "open_worksheet", mock_open_worksheet):
                with patch.object(google_spreadsheet, "append_rows_to_worksheet", mock_append_rows):
                    uploader.upload_jobs(jobs_for_upload)

        mock_get_new_jobs.assert_called_once_with(jobs_for_upload)
        mock_open_worksheet.assert_called_once()
        mock_append_rows.assert_called_once_with(jobs_for_upload, mock_worksheet)

    def test_upload_jobs_empty_list(self):
        uploader = create_default_uploader()
        mock_get_new_jobs = MagicMock()

        mock_open_worksheet = MagicMock()
        mock_worksheet = object()
        mock_open_worksheet.return_value = mock_worksheet

        mock_append_rows = MagicMock()

        with patch.object(uploader, "get_new_jobs", mock_get_new_jobs):
            with patch.object(uploader, "open_worksheet", mock_open_worksheet):
                with patch.object(google_spreadsheet, "append_rows_to_worksheet", mock_append_rows):
                    uploader.upload_jobs([])

        mock_get_new_jobs.assert_not_called()
        mock_open_worksheet.assert_not_called()
        mock_append_rows.assert_not_called()
