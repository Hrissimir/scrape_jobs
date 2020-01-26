import csv
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Set

from hed_utils.support import google_spreadsheet

__all__ = [
    "AStorage",
    "CsvJobsStorage",
    "GoogleSheetsJobsStorage"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class AStorage(ABC):

    def __init__(self, columns: List[str]):
        self.columns = columns

    def convert_to_rows(self, jobs: List[Dict[str, str]]) -> List[List[str]]:
        _log.debug("converting %s jobs to rows... (columns: %s)", len(jobs), self.columns)
        return [[j.get(col, "") for col in self.columns] for j in jobs]

    @abstractmethod
    def get_known_jobs_urls(self) -> Set[str]:
        """Return urls of jobs that are already stored.(Used for filtering duplicate records)"""

        pass

    @abstractmethod
    def store_jobs(self, jobs: List[Dict[str, str]]):
        """Store the processed jobs data to the backing storage"""

        pass


class CsvJobsStorage(AStorage):

    def __init__(self, columns: List[str], filepath: str, ):
        super().__init__(columns)
        self.urls_column_index = columns.index("url")
        self.filepath = Path(filepath).absolute()
        _log.info("initialized %s: columns=%s, urls_column_index=%s, filepath='%s'",
                  type(self).__name__, columns, self.urls_column_index, str(self.filepath))

    def init_file(self):
        _log.debug("initializing jobs csv: columns=%s, file='%s'", self.columns, str(self.filepath))
        with self.filepath.open(mode="w") as fp:
            writer = csv.writer(fp)
            writer.writerow(self.columns)

    def get_known_jobs_urls(self) -> Set[str]:
        _log.debug("getting known jobs urls from csv...")
        with self.filepath.open(mode="r") as fp:
            reader = csv.reader(fp)
            try:
                _ = next(reader)  # skip header
                known_jobs_urls = {row[self.urls_column_index] for row in reader}
            except StopIteration:
                known_jobs_urls = set()

        _log.debug("got %s known jobs urls", len(known_jobs_urls))
        return known_jobs_urls

    def store_jobs(self, jobs: List[Dict[str, str]]):
        rows = self.convert_to_rows(jobs)
        _log.debug("appending %s rows to csv at: %s", len(jobs), str(self.filepath))
        with self.filepath.open(mode="a") as fp:
            writer = csv.writer(fp)
            writer.writerows(rows)


class GoogleSheetsJobsStorage(AStorage):

    def __init__(self, columns: List[str], spreadsheet_title: str, worksheet_title: str, json_filepath: str):
        super().__init__(columns)
        self.urls_column_index = columns.index("url") + 1  # 1-based index
        self.worksheet = google_spreadsheet.open_worksheet(spreadsheet_title=spreadsheet_title,
                                                           worksheet_title=worksheet_title,
                                                           json_filepath=json_filepath)

        _log.info("initialized %s: "
                  "columns=%s, urls_column_index=%s, spreadsheet_title='%s', worksheet_title='%s', json_filepath='%s'",
                  type(self).__name__,
                  columns, self.urls_column_index, spreadsheet_title, worksheet_title, json_filepath)

    def get_known_jobs_urls(self) -> Set[str]:
        _log.debug("getting known jobs urls from worksheet...")
        known_jobs_urls = set(self.worksheet.col_values(self.urls_column_index))
        _log.debug("got %s known jobs urls", len(known_jobs_urls))
        return known_jobs_urls

    def store_jobs(self, jobs: List[Dict[str, str]]):
        rows = self.convert_to_rows(jobs)
        _log.debug("appending %s jobs to worksheet: %s", len(rows), self.worksheet)
        google_spreadsheet.append_worksheet_values(worksheet=self.worksheet, values=rows)
