from typing import List

from scrape_jobs.common2.job_result import JobResult


class JobsResultsPage:

    def has_results(self) -> bool:
        raise NotImplementedError()

    def has_next_page(self) -> bool:
        raise NotImplementedError()

    def get_visible_results(self) -> List[JobResult]:
        raise NotImplementedError()

    def go_to_next_page(self):
        raise NotImplementedError()
