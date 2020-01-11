import logging

from hed_utils.selenium import SharedDriver

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class BasePage:
    def __init__(self, url: str, search_params: dict):
        self.url = url
        self.search_params = search_params
        self.driver = SharedDriver()

    def go_to(self):
        _log.info("navigating to: %s", self.url)
        self.driver.get(self.url)

    def enter_search_params(self):
        _log.info("setting params: %s", self.search_params)

    def trigger_search(self):
        _log.info("triggering search...")

    def wait_for_results(self):
        _log.info("waiting for results...")

    def get_visible_jobs(self) -> list:
        _log.info("getting visible results...")

    def has_more_results(self) -> bool:
        _log.info("checking if more results are present...")

    def load_more_results(self):
        _log.info("loading more results...")
