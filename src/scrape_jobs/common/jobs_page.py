from abc import ABC

from hed_utils.selenium.page_objects.base.web_page import WebPage

from scrape_jobs.common.jobs_results_page import JobsResultsPage
from scrape_jobs.common.jobs_search_page import JobsSearchPage


class JobsPage(JobsSearchPage, JobsResultsPage, WebPage, ABC):
    def __init__(self, *, url_domain="", url_path=""):
        super().__init__(url_domain=url_domain, url_path=url_path)
