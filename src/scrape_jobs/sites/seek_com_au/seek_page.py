from scrape_jobs.common.jobs_page import JobsPage
from scrape_jobs.sites.seek_com_au.seek_jobs_results_page import SeekJobsResultsPage
from scrape_jobs.sites.seek_com_au.seek_search_context import SeekSearchContext


class SeekPage(SeekSearchContext, SeekJobsResultsPage, JobsPage):
    def __init__(self):
        super().__init__(url_domain="https://www.seek.com.au/", url_path="/")
