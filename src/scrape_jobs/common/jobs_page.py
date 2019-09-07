from abc import ABC

from hed_utils.selenium.page_objects.base.web_page import WebPage

from scrape_jobs.common.results_context import ResultsContext
from scrape_jobs.common.search_context import SearchContext


class JobsPage(SearchContext, ResultsContext, WebPage, ABC):
    pass
