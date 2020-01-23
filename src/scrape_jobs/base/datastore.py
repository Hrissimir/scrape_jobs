import logging
from abc import ABC, abstractmethod
from typing import List, Set, Type, TypeVar

from hed_utils.support import google_spreadsheet

from scrape_jobs.base.config import SheetsConfig
from scrape_jobs.base.job import Job

__all__ = [
    "JobTypeVar",
    "Datastore",
    "SheetsDatastore",
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

JobTypeVar = TypeVar("JobTypeVar", bound=Job)


class Datastore(ABC):

    @abstractmethod
    def get_known_jobs_urls(self) -> Set[str]:
        _log.debug("getting known jobs urls...")
        pass

    @abstractmethod
    def add_jobs(self, jobs: List[JobTypeVar]):
        _log.debug("adding %s new jobs to %s", len(jobs), self)


class SheetsDatastore(Datastore):

    def __init__(self, *, config: SheetsConfig, job_cls: Type[JobTypeVar]):
        assert issubclass(job_cls, Job)
        self.config = config
        self.job_cls = job_cls
        self.columns = [key.upper() for key in job_cls.keys()]
        self.worksheet = google_spreadsheet.open_worksheet(spreadsheet_title=config.spreadsheet_title,
                                                           worksheet_title=config.worksheet_title,
                                                           json_filepath=config.json_filepath)

    def __repr__(self):
        return f"{type(self).__name__}(config={self.config}, job_cls={self.job_cls.__name__})"

    def get_known_jobs_urls(self) -> Set[str]:
        super().get_known_jobs_urls()
        column_index = self.columns.index("URL") + 1
        known_jobs_urls = set(self.worksheet.col_values(column_index))
        _log.info("got %s known jobs urls!", len(known_jobs_urls))
        return known_jobs_urls

    def add_jobs(self, jobs: List[Job]):
        super().add_jobs(jobs)
        google_spreadsheet.append_worksheet_values(worksheet=self.worksheet, values=[job.values() for job in jobs])
        _log.info("added %s jobs to %s", len(jobs), self)
