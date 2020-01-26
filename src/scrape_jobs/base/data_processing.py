import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from hed_utils.support.time_tool import get_local_tz_name, utc_to_tz

__all__ = [
    "AProcessor",
    "TimeProcessor"
]
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class AProcessor(ABC):

    def process_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Process the collected jobs and prepare them for upload (e.g. format datetime values)"""

        processed_jobs = []
        for raw in jobs:
            try:
                processed = self.process_job(raw)
            except BaseException as err:
                _log.warning("Error while processing record '%s'! (%s) %s", raw, type(err).__name__, err)
                continue

            processed_jobs.append(processed)

        return processed_jobs

    @abstractmethod
    def process_job(self, job: Dict[str, Any]) -> Dict[str, str]:
        pass


class TimeProcessor(AProcessor):
    """Performs UTC to timezone conversion of scraped/posted times and applies desired formatting"""

    def __init__(self, tz_name: str = None, scraped_fmt: str = None, posted_fmt: str = None):
        super().__init__()
        self.tz_name = tz_name or get_local_tz_name()
        self.scraped_fmt = scraped_fmt or "%Y-%m-%d %H:%M"
        self.posted_fmt = posted_fmt or "%Y-%m-%d %H:%M"

    def process_job(self, job: Dict[str, Any]) -> Dict[str, str]:
        if "posted_time" in job:
            utc_posted = job["posted_time"]
            if utc_posted:
                job["posted_time"] = utc_to_tz(utc_posted, self.tz_name).strftime(self.posted_fmt)
        if "scraped_time" in job:
            utc_scraped = job["scraped_time"]
            if utc_scraped:
                job["scraped_time"] = utc_to_tz(utc_scraped, self.tz_name).strftime(self.posted_fmt)

        return {key: (str(value) if value else "") for key, value in job.items()}
