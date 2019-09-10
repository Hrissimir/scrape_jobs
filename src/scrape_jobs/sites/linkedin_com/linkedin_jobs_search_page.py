from hed_utils.selenium import driver
from hed_utils.support import log

from scrape_jobs.common.jobs_search_page import JobsSearchPage
from scrape_jobs.sites.linkedin_com.linkedin_jobs_results_page import LinkedinJobsResultsPage
from scrape_jobs.sites.linkedin_com.linkedin_search_filters import DatePostedFilter
from scrape_jobs.sites.linkedin_com.linkedin_search_section import LinkedinSearchSection, LinkedinJobsSearchForm, \
    LinkedinJobsSearchBar


class LinkedinJobsSearchPage(JobsSearchPage):
    JOBS_SEARCH_FORM = LinkedinJobsSearchForm()
    JOBS_SEARCH_BAR = LinkedinJobsSearchBar()
    DATE_POSTED_FILTER = DatePostedFilter()

    JOBS_RESULTS = LinkedinJobsResultsPage()

    def get_search_section(self) -> LinkedinSearchSection:
        if self.JOBS_SEARCH_FORM.is_visible():
            return self.JOBS_SEARCH_FORM
        elif self.JOBS_SEARCH_BAR.is_visible():
            return self.JOBS_SEARCH_BAR
        else:
            raise RuntimeError("neither the search-form, nor the search-bar were present")

    def trigger_search(self):
        self.get_search_section().trigger_search()

    def set_search_params(self, **params):
        log.debug("setting linkedin jobs search params: %s", params)

        keywords = params.pop("keywords", None)
        if keywords:
            self.get_search_section().set_keywords(keywords)

        location = params.pop("location", None)
        if location:
            self.get_search_section().set_location(location)

        date_posted = params.pop("date_posted", None)
        if date_posted:
            self.DATE_POSTED_FILTER.set_date_posted(date_posted)

    def wait_for_search_complete(self):
        driver.wait_until_visible_element(self.JOBS_RESULTS.LOCATOR)
