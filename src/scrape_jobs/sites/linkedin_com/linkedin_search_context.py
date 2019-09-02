from hed_utils.selenium.page_objects.base.web_page import WebPage
from hed_utils.support import log

from scrape_jobs.common.search_context import SearchContext
from scrape_jobs.sites.linkedin_com.linkedin_jobs_search_bar import LinkedinJobsSearchBar
from scrape_jobs.sites.linkedin_com.linkedin_jobs_search_form import LinkedinJobsSearchForm
from scrape_jobs.sites.linkedin_com.linkedin_results_context import LinkedinResultsContext
from scrape_jobs.sites.linkedin_com.linkedin_search_section import LinkedinSearchSection


class LinkedinSearchContext(SearchContext):
    JOBS_SEARCH_FORM = LinkedinJobsSearchForm()
    JOBS_SEARCH_BAR = LinkedinJobsSearchBar()
    JOBS_RESULTS = LinkedinResultsContext()

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

    def set_location(self, location):
        self.search_section.set_location(location)

    def trigger_search(self):
        self.search_section.trigger_search()

    def set_search_params(self, **params):
        log.info("setting linkedin jobs search params: %s", params)

        keywords = params.pop("keywords", "")
        self.set_keywords(keywords)

        location = params.pop("location", "")
        self.set_location(location)

    def wait_for_search_complete(self):
        self.JOBS_RESULTS.wait_to_appear()
