from abc import ABC, abstractproperty
from typing import Tuple

from hed_utils.selenium import driver
from hed_utils.selenium.page_objects.base.page_element import PageElement
from hed_utils.support import log


class LinkedinSearchSection(PageElement, ABC):
    @abstractproperty
    def keywords_input_locator(self) -> Tuple[str, str]:
        pass

    @abstractproperty
    def location_input_locator(self) -> Tuple[str, str]:
        pass

    @abstractproperty
    def search_button_locator(self) -> Tuple[str, str]:
        pass

    def set_keywords(self, keywords):
        log.info("setting search keywords to: '%s'", keywords)
        driver.set_text(self.keywords_input_locator, keywords, press_enter=True)

    def set_location(self, location):
        log.info("setting search location to: '%s'", location)
        driver.set_text(self.location_input_locator, location, press_enter=True)

    def trigger_search(self):
        log.info("triggering search...")
        driver.wait_until_page_loads()
        driver.scroll_into_view(self.search_button_locator)
        driver.wait_until_page_loads()
        driver.click_element(self.search_button_locator)
