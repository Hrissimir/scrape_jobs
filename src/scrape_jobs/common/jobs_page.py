from abc import ABC
from typing import List

from hed_utils.selenium.page_objects.base.web_page import WebPage
from hed_utils.support import log

from scrape_jobs.common.result_predicate import ResultPredicate
from scrape_jobs.common.results_context import ResultsContext
from scrape_jobs.common.search_context import SearchContext


class JobsPage(SearchContext, ResultsContext, WebPage, ABC):

    def search_and_collect(self, predicate: ResultPredicate, **search_params) -> List[dict]:
        log.info("collecting jobs from '%s' (search_params: %s)", type(self).__name__, search_params)

        self.go_to(wait_for_url_changes=False, wait_for_page_load=True)

        self.set_search_params(**search_params)
        self.trigger_search()
        self.wait_for_search_complete()

        known_results_dicts = []

        matching_results_dicts = []

        is_first_time_no_jobs = True

        while self.has_results():
            all_results_dicts = [result.as_dict()
                                 for result
                                 in self.get_visible_results()]
            log.info("   total results: %s", len(all_results_dicts))

            new_results_dicts = [result_dict
                                 for result_dict
                                 in all_results_dicts
                                 if (result_dict not in known_results_dicts)]
            log.info("     new results: %s", len(new_results_dicts))
            known_results_dicts.extend(new_results_dicts)

            matching_new_results_dicts = [result_dict
                                          for result_dict
                                          in new_results_dicts
                                          if predicate(result_dict)]
            log.info("matching results: %s", len(matching_new_results_dicts))

            if matching_new_results_dicts:
                matching_results_dicts.extend(matching_new_results_dicts)
                is_first_time_no_jobs = True
            else:
                log.warning("there were no matching new results!")
                if is_first_time_no_jobs:
                    log.warning("first time no matching results - will stop iteration next time")
                    is_first_time_no_jobs = False
                else:
                    log.warning("second time no matching results - done iterating!")
                    break

            if self.has_next_page():
                self.go_to_next_page()
                self.wait_for_search_complete()
            else:
                log.info("done with jobs collection (no Next results page present)")
                break

        return matching_results_dicts
