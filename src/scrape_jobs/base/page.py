import logging
from abc import ABC, abstractmethod
from typing import List

from bs4 import Tag
from hed_utils.selenium import SharedDriver, chrome_driver

from scrape_jobs.base.job import Job

__all__ = [
    "Page",
    "init_driver"
]
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def init_driver(headless: bool):
    _log.info("initializing driver: headless=%s", headless)
    driver = chrome_driver.create_instance(headless=headless)
    driver.set_page_load_timeout(30)
    SharedDriver.set_instance(driver)


class Page(ABC):
    driver = SharedDriver()

    def __repr__(self):
        return type(self).__name__

    @classmethod
    @abstractmethod
    def get_visible_job_tags(cls, page_source: str) -> List[Tag]:
        _log.debug("getting visible job tags... (page-source chars: %s)", len(page_source))

    @classmethod
    @abstractmethod
    def parse_job_tag(cls, tag: Tag) -> Job:
        pass

    @classmethod
    def get_visible_jobs(cls) -> List[Job]:
        _log.debug("getting visible jobs...")
        visible_jobs = [cls.parse_job_tag(tag)
                        for tag
                        in cls.get_visible_job_tags(cls.driver.page_source)]
        _log.info("visible jobs: %s", len(visible_jobs))
        return visible_jobs

    @abstractmethod
    def go_to(self):
        _log.info("navigating to: %s", self)

    @abstractmethod
    def set_search_params(self, search_params: dict):
        _log.info("setting search params to: %s", search_params)
        pass

    @abstractmethod
    def trigger_search(self):
        _log.info("triggering search...")
        pass

    @abstractmethod
    def wait_for_results_to_load(self):
        _log.info("waiting for results to load...")
        pass

    @abstractmethod
    def has_more_results(self) -> bool:
        _log.info("checking if more results are available...")

    @abstractmethod
    def load_more_results(self):
        _log.info("loading more results...")
        pass
