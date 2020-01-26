import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from operator import itemgetter
from typing import Dict, Any, List, Set

from bs4 import Tag, BeautifulSoup
from hed_utils.selenium import SharedDriver
from hed_utils.support.time_tool import utc_moment
from tabulate import tabulate

__all__ = [
    "ACollector",
    "JobParser",
    "Page"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def format_jobs(jobs: List[Dict[str, Any]], skip_keys: Set[str] = None) -> str:
    skip_keys = skip_keys or {"posted_time", "scraped_time"}
    data = [{k: v for k, v in j.items() if k not in skip_keys} for j in jobs]
    return tabulate(data, headers={key: key.upper() for key in jobs[0].keys()})


class ACollector(ABC):

    @abstractmethod
    def collect_jobs(self) -> List[Dict[str, Any]]:
        """Collect the data and return it as list of dicts with string-only keys and values of any type"""

        pass


class JobParser(ABC):
    KEYS: List[str]
    SELECTOR: str

    def __init__(self):
        self.creation_time_utc = utc_moment().replace(second=0, microsecond=0)
        self.known_tags = set()

    def find_all(self, page_soup: BeautifulSoup) -> List[Tag]:
        _log.debug("getting job tags...")
        job_tags = page_soup.select(self.SELECTOR) or []
        _log.debug("got %s job tags", len(job_tags))
        return job_tags

    def find_new(self, page_soup: BeautifulSoup, memoize=True):
        new_tags = [tag for tag in self.find_all(page_soup) if tag not in self.known_tags]
        _log.debug("got %s new tags", len(new_tags))
        if memoize:
            self.known_tags.update(new_tags)
        return new_tags

    @abstractmethod
    def parse(self, tag: Tag) -> Dict[str, Any]:
        return {key: None for key in self.KEYS}


class Page(ACollector, ABC):
    PAGE_URL: str
    driver = SharedDriver()

    def __init__(self,
                 search_params: Dict[str, Any],
                 max_post_age_days: int,
                 max_attempts: int,
                 parser: JobParser):
        self.search_params = search_params
        self.utc_posted_after = self.calc_utc_posted_after(max_post_age_days)
        self.max_attempts = max_attempts
        self.parser = parser
        _log.info("initialized %s: max_post_age_days=%s, max_attempts=%s, utc_posted_after=%s, search_params=%s",
                  type(self).__name__, max_post_age_days, max_attempts, self.utc_posted_after, search_params)

    @classmethod
    def calc_utc_posted_after(cls, days_ago: int) -> datetime:
        try:
            return utc_moment().replace(minute=0, second=0, microsecond=0) - timedelta(days=days_ago)
        except Exception as err:
            _log.exception("error while calculating utc_posted_after! (%s) %s", type(err).__name__, err)
            raise

    @property
    def visible_jobs_count(self) -> int:
        return len(self.parser.find_all(self.driver.page_soup))

    @abstractmethod
    def perform_search(self):
        pass

    @abstractmethod
    def wait_for_results_to_load(self):
        pass

    @abstractmethod
    def has_more_results(self) -> bool:
        pass

    @abstractmethod
    def load_more_results(self):
        pass

    def get_visible_results(self) -> List[Dict[str, Any]]:
        tags = self.parser.find_new(self.driver.page_soup)
        return [self.parser.parse(tag) for tag in tags]

    def collect_jobs(self) -> List[Dict[str, Any]]:
        _log.info("navigating to page: %s", self.PAGE_URL)
        self.driver.get(self.PAGE_URL)

        _log.info("performing search...")
        self.perform_search()

        collected_results = []
        known_results = []

        remaining_attempts = self.max_attempts
        while remaining_attempts > 0:
            _log.info("waiting for results to load...")
            self.wait_for_results_to_load()

            _log.info("getting visible results...")
            visible_results = self.get_visible_results()
            _log.info("visible results: %s", len(visible_results))

            if not visible_results:
                _log.warning("no visible results were present! Exiting loop...")
                break

            unknown_results = [vr for vr in visible_results if vr not in known_results]
            _log.info("unknown results: %s", len(unknown_results))
            known_results.extend(unknown_results)

            recent_results = [result
                              for result
                              in unknown_results
                              if (result.get("posted_time", None) is not None
                                  and result["posted_time"] > self.utc_posted_after)]
            _log.info("recent  results: %s", len(recent_results))

            if recent_results:
                collected_results.extend(recent_results)
                remaining_attempts = self.max_attempts
                _log.info("\n\n\n%s\n\n\n", format_jobs(recent_results))
            else:
                remaining_attempts -= 1
                _log.warning("no new results were collected in this iteration! remaining attempts: %s",
                             remaining_attempts)

            if self.has_more_results():
                _log.info("loading more results...")
                self.load_more_results()
            else:
                _log.warning("no more results to load! Exiting loop...")
                break

        _log.info("total of %s results collected!", len(collected_results))
        collected_results.sort(key=itemgetter("posted_time"))
        return collected_results
