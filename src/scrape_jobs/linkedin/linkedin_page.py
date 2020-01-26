import logging
from typing import Dict, Any

from hed_utils.selenium import FindBy, SharedDriver
from hed_utils.support.text_tool import normalize_spacing
from hed_utils.support.time_tool import poll_for_result
from selenium.webdriver.common.keys import Keys

from scrape_jobs.base.data_collection import Page
from scrape_jobs.linkedin import LinkedinJob

__all__ = ["LinkedinPage"]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class LinkedinPage(Page):
    PAGE_URL = "https://www.linkedin.com/jobs"

    def __init__(self, search_params: Dict[str, Any], max_post_age_days: int, max_attempts: int):
        super().__init__(search_params, max_post_age_days, max_attempts, parser=LinkedinJob())
        self._keywords_input = FindBy.NAME("keywords", visible_only=True)
        self._location_input = FindBy.NAME("location", visible_only=True)
        self._search_button = FindBy.CSS_SELECTOR("button[type='submit'][aria-label='Search']", visible_only=True)
        self._see_more_jobs_button = FindBy.CSS_SELECTOR("button.see-more-jobs", visible_only=True)
        self._search_results = FindBy.CSS_SELECTOR("section.results__list > ul > li.result-card", visible_only=True)
        self._date_posted_filter = DatePostedFilter()

    def perform_search(self):
        self.set_search_params()

    def set_search_params(self):
        _log.info("setting search params...")
        search_params = self.search_params

        keywords = search_params.get("keywords", "")
        _log.info("entering 'keywords': '%s'", keywords)
        self._keywords_input.click()
        self._keywords_input.send_keys(keywords + Keys.ENTER)
        self.driver.wait_for_page_load()

        location = search_params.get("location", "")
        _log.info("entering 'location': '%s'", location)
        self._location_input.click()
        self._location_input.clear()
        self._location_input.send_keys(location + Keys.ENTER)
        self.driver.wait_for_page_load()

        date_posted = search_params.get("date_posted", "")
        _log.info("applying 'date-posted' filter: '%s'", date_posted)
        self._date_posted_filter.set_value(date_posted)

    def wait_for_results_to_load(self):
        self.driver.wait_for_page_load()
        return self._search_results.is_visible(timeout=20)

    def has_more_results(self) -> bool:
        self.scroll_to_bottom()
        return self._see_more_jobs_button.is_visible(timeout=10)

    def load_more_results(self):
        initial_results_count = self.visible_jobs_count

        def more_results_loaded():
            return initial_results_count < self.visible_jobs_count

        self._see_more_jobs_button.click()
        self.driver.wait_for_page_load()

        poll_for_result(more_results_loaded, timeout_seconds=10, poll_frequency=1)

    def scroll_to_bottom(self):
        _log.debug("scrolling last result into view...")
        if self._search_results.is_visible():
            search_results = self._search_results.elements
            if search_results:
                search_results[-1].scroll_into_view()
                self.driver.wait_for_page_load()
        else:
            _log.debug("can't scroll to bottom! (no results)")


class DatePostedFilter:

    def __init__(self):
        self._driver = SharedDriver()
        self._open_filter_button = FindBy.XPATH("//div[@id='TIME_POSTED-dropdown']/../button")
        self._filter_body = FindBy.CSS_SELECTOR("div#TIME_POSTED-dropdown")
        self._filter_value_label = FindBy.XPATH(
            "//div[@id='TIME_POSTED-dropdown']//div[contains(@class, 'filter-list')]/ul/li/label")
        self._apply_button = FindBy.XPATH(
            "//div[contains(@class, 'dropdown-actions')]/button[contains(@class,'apply')]")

    def _open_chooser(self):
        _log.debug("opening date-posted filter")
        self._open_filter_button.click()

        if not self._filter_value_label.is_visible(timeout=5):
            raise RuntimeError("Could not open 'Date-Posted' filter!")

    def _close_chooser(self):
        _log.debug("closing date-posted filter...")
        self._apply_button.click()
        self._filter_body.wait_until_gone(timeout=5)
        self._driver.wait_for_page_load()

    def _choose_value(self, value: str):
        _log.debug("selecting date-posted value: '%s'", value)
        visible_labels = []
        for label in self._filter_value_label:
            label_text = normalize_spacing(label.text.strip())
            if value.lower() in label_text.lower():
                label_input = label.parent_element.find_element_by_tag_name("input")
                self._driver.execute_script("arguments[0].click();", label_input.wrapped_element)
                return
            else:
                visible_labels.append(label_text)

        _log.warning("visible date-posted filter values: %s", visible_labels)
        raise RuntimeError("Could not click Date-Posted filter value!", value, visible_labels)

    def set_value(self, value: str):
        self._open_chooser()
        self._choose_value(value)
        self._close_chooser()
