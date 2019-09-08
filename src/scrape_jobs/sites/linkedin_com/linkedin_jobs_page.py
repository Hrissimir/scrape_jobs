from scrape_jobs.common.jobs_page import JobsPage
from scrape_jobs.sites.linkedin_com.linkedin_jobs_results_page import LinkedinJobsResultsPage
from scrape_jobs.sites.linkedin_com.linkedin_jobs_search_page import LinkedinJobsSearchPage


class LinkedinJobsPage(LinkedinJobsSearchPage, LinkedinJobsResultsPage, JobsPage):
    def __init__(self):
        super().__init__(url_domain="https://www.linkedin.com/", url_path="/jobs")
