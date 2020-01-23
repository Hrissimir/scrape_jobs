from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, NoReturn, Optional, Union

from hed_utils.support.time_tool import utc_to_tz
from tabulate import tabulate

from scrape_jobs.base.config import TimeConfig

__all__ = [
    "Job",
    "format_jobs"
]


class Job(ABC):
    company: str
    title: str
    url: str
    posted_time: Union[str, datetime]
    scraped_time: Union[str, datetime]

    @classmethod
    @abstractmethod
    def keys(cls) -> List[str]:
        pass

    def prepare_for_upload(self, *, time_config: Optional[TimeConfig] = None) -> NoReturn:
        if time_config:
            self.scraped_time = utc_to_tz(self.scraped_time, time_config.tz_name).strftime(time_config.scraped_fmt)
            self.posted_time = utc_to_tz(self.posted_time, time_config.tz_name).strftime(time_config.posted_fmt)

    def values(self) -> List[Any]:
        return [getattr(self, key) for key in self.keys()]

    def as_dict(self) -> Dict[str, Any]:
        return dict(zip(self.keys(), self.values()))


def format_jobs(jobs: List[Job]) -> str:
    return tabulate(tabular_data=[j.as_dict() for j in jobs],
                    headers="keys",
                    stralign="left")
