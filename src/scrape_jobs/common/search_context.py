from abc import ABC


class SearchContext(ABC):

    def set_search_params(self, **params):
        raise NotImplementedError()

    def trigger_search(self):
        raise NotImplementedError()

    def wait_for_search_complete(self):
        raise NotImplementedError()
