from abc import ABC
from typing import List

from hed_utils.support import waiter

from scrape_jobs.common.job_result import JobResult


class JobsResultsPage(ABC):

    def has_results(self) -> bool:
        raise NotImplementedError()

    def has_next_page(self) -> bool:
        raise NotImplementedError()

    def get_visible_results(self) -> List[JobResult]:
        raise NotImplementedError()

    def go_to_next_page(self):
        raise NotImplementedError()

    def wait_for_results(self):
        waiter.poll_for_result(self.has_results, timeout_seconds=30, default=TimeoutError)
