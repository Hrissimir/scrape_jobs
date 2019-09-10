from hed_utils.selenium import driver
from hed_utils.selenium.page_objects.base.page_element import PageElement
from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper
from hed_utils.support import log, waiter
from selenium.webdriver.common.by import By


class SearchFilter(PageElement):
    _LOCATOR = "//li[contains(@class,'top-filters__item')]/div/button[contains(.,'{text}')]/../.."

    MODAL_LOCATOR = By.XPATH, "//div[contains(@class,'filter-dropdown__dropdown')]"
    DONE_BUTTON = By.XPATH, "//div[contains(@class, 'filter-button-dropdown__dropdown-actions')]/button"

    def __init__(self, name):
        self.name = name
        super().__init__(locator=(By.XPATH, self._LOCATOR.format(text=name)))

    def button(self) -> ElementWrapper:
        return self.get_element().find_element_by_xpath("./div/button")

    @property
    def modal(self) -> ElementWrapper:
        return driver.wait_until_visible_element(self.MODAL_LOCATOR)

    def is_opened(self) -> bool:
        return driver.is_visible(self.MODAL_LOCATOR)

    def apply(self):
        log.info("applying '%s' filter", self.name)
        driver.click_locator(self.DONE_BUTTON)
        driver.wait_until_page_loads()

    def open_modal(self):
        log.info("opening modal for filter: '%s'", self.name)
        if not self.is_opened():
            self.button().click()
            error = TimeoutError(f"The modal of '{self.name}' filter did not appear")
            waiter.poll_for_result(self.is_opened, timeout_seconds=10, default=error)

    def click_option(self, name):
        log.info("clicking option: '%s' ", name)
        option_locator = By.XPATH, self.MODAL_LOCATOR[
            -1] + f"//label[contains(@class,'filter-list__list-item-label')][contains(.,'{name}')]"
        driver.click_locator(option_locator)


class DatePostedFilter(SearchFilter):
    PAST_24_HOURS = "Past 24 hours"
    PAST_WEEK = "Past Week"
    PAST_MONTH = "Past Month"
    ANY_TIME = "Any Time"

    def __init__(self):
        super().__init__("Date Posted")

    @classmethod
    def values(cls):
        return [cls.PAST_24_HOURS, cls.PAST_WEEK, cls.PAST_MONTH, cls.ANY_TIME]

    def set_date_posted(self, value):
        log.info("setting date posted filter: '%s'", value)
        if value not in self.values():
            raise ValueError(f"Unsupported value: '%s'! (%s)", value, self.values())
        self.open_modal()
        self.click_option(value)
        self.apply()
