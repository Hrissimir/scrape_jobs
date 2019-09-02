from scrape_jobs.common.jobs_page import JobsPage
from scrape_jobs.sites.linkedin_com.linkedin_results_context import LinkedinResultsContext
from scrape_jobs.sites.linkedin_com.linkedin_search_context import LinkedinSearchContext


class LinkedinJobsPage(LinkedinSearchContext, LinkedinResultsContext, JobsPage):
    def __init__(self):
        super().__init__(url_domain="https://www.linkedin.com/", url_path="/jobs")
