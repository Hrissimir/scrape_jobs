import logging
from datetime import datetime
from operator import attrgetter
from typing import Set, List

from scrape_jobs.base.job import Job, format_jobs
from scrape_jobs.base.page import Page

__all__ = [
    "Scraper"
]
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class Scraper:
    MAX_ATTEMPTS = 5
    SORT_BY = attrgetter("posted_time")

    def __init__(self, *, page: Page, search_params: dict, utc_posted_after: datetime, known_jobs_urls: Set[str]):
        self.page = page
        self.search_params = search_params
        self.utc_posted_after = utc_posted_after
        self.known_jobs_urls = known_jobs_urls

    def scrape(self) -> List[Job]:
        page = self.page
        known_jobs_urls = self.known_jobs_urls
        utc_posted_after = self.utc_posted_after
        scraped_jobs = []

        page.go_to()
        page.set_search_params(self.search_params)
        page.trigger_search()

        remaining_attempts = self.MAX_ATTEMPTS
        while remaining_attempts > 0:
            page.wait_for_results_to_load()

            visible_jobs = page.get_visible_jobs()

            unknown_jobs = [j for j in visible_jobs if j.url not in known_jobs_urls]
            _log.info("unknown jobs: %s", len(unknown_jobs))

            jobs_with_post_time = [j for j in unknown_jobs if j.posted_time]
            _log.info("jobs with 'post time': %s", len(jobs_with_post_time))

            recent_jobs = [j for j in jobs_with_post_time if j.posted_time > utc_posted_after]
            _log.info("recent jobs: %s", len(recent_jobs))

            new_jobs = recent_jobs
            if new_jobs:
                remaining_attempts = self.MAX_ATTEMPTS
                _log.info("got %s new jobs from page!\n%s", len(new_jobs), format_jobs(new_jobs))
                scraped_jobs.extend(new_jobs)
                known_jobs_urls.update(job.url for job in new_jobs)
            else:
                remaining_attempts -= 1
                _log.warning("no new jobs we present on page! (remaining attempts: %s)", remaining_attempts)

            if page.has_more_results():
                page.load_more_results()
                continue

            _log.warning("no more new jobs to load!")
            break

        scraped_jobs.sort(key=self.SORT_BY)
        return scraped_jobs
