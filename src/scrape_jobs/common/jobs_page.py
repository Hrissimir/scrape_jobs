from abc import ABC
from pprint import pformat
from typing import List, Dict

from hed_utils.selenium.page_objects.base.web_page import WebPage
from hed_utils.support import log, waiter

JobsData = List[Dict[str, str]]


class ISearchContext(ABC):

    def set_search_params(self, **params):
        raise NotImplementedError()

    def trigger_search(self):
        raise NotImplementedError()

    def wait_for_search_complete(self):
        raise NotImplementedError()


class IResultsContext(ABC):

    def has_results(self) -> bool:
        raise NotImplementedError()

    def has_next_page(self) -> bool:
        raise NotImplementedError()

    def get_visible_results(self) -> List[dict]:
        raise NotImplementedError()

    def go_to_next_page(self):
        raise NotImplementedError()

    def wait_for_results(self):
        waiter.poll_for_result(self.has_results, timeout_seconds=30, default=TimeoutError)


class JobsPage(ISearchContext, IResultsContext, WebPage, ABC):
    pass


def search_and_collect(page: JobsPage, job_predicate, **search_params) -> List[dict]:
    log.info("collecting jobs from '%s' (search_params: %s)", type(page).__name__, search_params)

    page.go_to(wait_for_url_changes=False, wait_for_page_load=True)

    page.set_search_params(**search_params)
    page.trigger_search()
    page.wait_for_search_complete()

    known_results = []
    results_of_interest = []

    is_first_time_no_jobs = True
    while page.has_results():

        new_results = [r for r in page.get_visible_results() if (r not in known_results)]
        new_interesting_results = [job for job in new_results if job_predicate(job)]

        if new_interesting_results:
            log.info("got %s new results:\n%s", len(new_interesting_results), pformat(new_interesting_results))
            results_of_interest.extend(new_interesting_results)
            is_first_time_no_jobs = True
        else:
            log.warning("there were no jobs of interest on this results page (out of %s jobs)", len(new_results))
            if is_first_time_no_jobs:
                log.warning("this was the first time it happened - will stop the search on next occasion")
                is_first_time_no_jobs = False
            else:
                log.warning("this was the second time it happened in a row - done iterating results!")
                break

        if page.has_next_page():
            page.go_to_next_page()
            page.wait_for_search_complete()
        else:
            log.info("done with jobs collection (no Next results page present)")
            break

    return results_of_interest
