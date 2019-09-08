from typing import Tuple

from hed_utils.selenium import driver
from hed_utils.support import log
from selenium.webdriver.common.by import By

from scrape_jobs.common.jobs_search_page import JobsSearchPage
from scrape_jobs.sites.linkedin_com.linkedin_jobs_results_page import LinkedinJobsResultsPage
from scrape_jobs.sites.linkedin_com.linkedin_search_filters import DatePostedFilter
from scrape_jobs.sites.linkedin_com.linkedin_search_section import LinkedinSearchSection


class LinkedinJobsSearchBar(LinkedinSearchSection):
    @property
    def keywords_input_locator(self) -> Tuple[str, str]:
        return self.KEYWORDS_INPUT

    @property
    def location_input_locator(self) -> Tuple[str, str]:
        return self.LOCATION_INPUT

    @property
    def search_button_locator(self) -> Tuple[str, str]:
        return self.SEARCH_BUTTON

    LOCATOR = By.XPATH, "//header//nav/section[@class='search-bar']"
    KEYWORDS_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'keywords')]"
    LOCATION_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'location')]"

    SEARCH_BUTTON = By.CSS_SELECTOR, "section[data-searchbar-type='JOBS'] button[type='submit']"

    def __init__(self):
        super().__init__(self.LOCATOR)


class LinkedinJobsSearchForm(LinkedinSearchSection):
    @property
    def keywords_input_locator(self) -> Tuple[str, str]:
        return self.KEYWORDS_INPUT

    @property
    def location_input_locator(self) -> Tuple[str, str]:
        return self.LOCATION_INPUT

    @property
    def search_button_locator(self) -> Tuple[str, str]:
        return self.SEARCH_BUTTON

    LOCATOR = By.XPATH, "//main//section//form[contains(@action,'/jobs/search')]"
    KEYWORDS_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'keywords')]"
    LOCATION_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'location')]"
    SEARCH_BUTTON = By.XPATH, "//button[contains(@form,'JOBS')]"

    def __init__(self):
        super().__init__(self.LOCATOR)


class LinkedinJobsSearchPage(JobsSearchPage):
    JOBS_SEARCH_FORM = LinkedinJobsSearchForm()
    JOBS_SEARCH_BAR = LinkedinJobsSearchBar()
    DATE_POSTED_FILTER = DatePostedFilter()

    JOBS_RESULTS = LinkedinJobsResultsPage()

    @property
    def search_section(self) -> LinkedinSearchSection:
        if self.JOBS_SEARCH_FORM.is_visible():
            return self.JOBS_SEARCH_FORM
        elif self.JOBS_SEARCH_BAR.is_visible():
            return self.JOBS_SEARCH_BAR
        else:
            raise RuntimeError("neither the search-form, nor the search-bar were present")

    def set_keywords(self, keywords):
        self.search_section.set_keywords(keywords)
        driver.wait_until_page_loads()

    def set_location(self, location):
        self.search_section.set_location(location)
        driver.wait_until_page_loads()

    def set_date_posted(self, date_posted):
        self.DATE_POSTED_FILTER.set_date_posted(date_posted)
        driver.wait_until_page_loads()

    def trigger_search(self):
        # no need to trigger - entering details re-triggers automatically

        return

    def set_search_params(self, **params):
        log.info("setting linkedin jobs search params: %s", params)

        keywords = params.pop("keywords", "")
        self.set_keywords(keywords)

        location = params.pop("location", "")
        self.set_location(location)

        date_posted = params.pop("date_posted", DatePostedFilter.PAST_MONTH)
        self.set_date_posted(date_posted)

    def wait_for_search_complete(self):
        driver.wait_until_visible_element(self.JOBS_RESULTS.LOCATOR)
