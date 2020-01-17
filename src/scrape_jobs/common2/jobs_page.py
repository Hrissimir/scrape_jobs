from urllib.parse import urljoin

from hed_utils.selenium import SharedDriver

from scrape_jobs.common2.jobs_results_page import JobsResultsPage
from scrape_jobs.common2.jobs_search_page import JobsSearchPage


class JobsPage(JobsSearchPage, JobsResultsPage):
    def __init__(self, *, url_domain="", url_path=""):
        self.url_domain = url_domain
        self.url_path = url_path

    def go_to(self, wait_for_url_changes=False, wait_for_page_load=True):
        SharedDriver.get_instance().get(urljoin(self.url_domain, self.url_path),
                                        wait_for_url_change=wait_for_url_changes,
                                        wait_for_page_load=wait_for_page_load)
