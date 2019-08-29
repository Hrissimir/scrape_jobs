from urllib.parse import urljoin

from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper


class SeekResult(ElementWrapper):

    def __init__(self, element):
        super().__init__(element)
        self._soup = self.soup
        self._dict = dict(date=self.job_date,
                          title=self.job_title,
                          company=self.job_company,
                          classification=self.job_classification,
                          salary=self.job_salary,
                          suburb=self.job_suburb,
                          url=self.job_url)

    @property
    def is_featured(self) -> bool:
        try:
            return self._soup.select_one("span[data-automation='jobPremium']") is not None
        except:
            return False

    @property
    def job_title(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobTitle']").get_text().strip()
        except:
            return "NO_TITLE"

    @property
    def job_url(self) -> str:
        try:
            a = self._soup.select_one("a[data-automation='jobTitle']")
            domain = "https://www.seek.com.au/"
            link = urljoin(domain, a["href"])
            return link[:link.index("?")]
        except:
            return "NO_URL"

    @property
    def job_date(self) -> str:
        from hed_utils.support import time_tool
        try:

            date = self._soup.select_one("span[data-automation='jobListingDate']").get_text().strip()
        except:
            if self.is_featured:
                return "Featured"
            else:
                return "NO_DATE"

        if date:
            date = time_tool.PastTimeParser.parse(date)
            tz_date = str(time_tool.convert_to_tz(date, "Australia/Sydney").date())
            return str(tz_date)

        return ""

    @property
    def _job_classification(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobClassification']").get_text().strip()
        except:
            return ""

    @property
    def _job_sub_classification(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobSubClassification']").get_text().strip()
        except:
            return ""

    @property
    def job_classification(self) -> str:
        components = [c for c in [self._job_classification, self._job_sub_classification] if c]
        return ", ".join(components)

    @property
    def job_company(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobCompany']").get_text().strip()
        except:
            return "NO_COMPANY"

    @property
    def job_salary(self) -> str:
        try:
            return self._soup.select_one("span[data-automation='jobSalary']").get_text().strip()
        except:
            return "NO_SALARY"

    @property
    def job_suburb(self) -> str:
        try:
            city = self._soup.select_one("a[data-automation='jobLocation']").get_text().strip()
        except:
            city = ""
        try:
            area = self._soup.select_one("a[data-automation='jobArea']").get_text().strip()
        except:
            area = ""

        components = [c for c in [city, area] if c]
        return ", ".join(components)

    def as_dict(self) -> dict:
        return self._dict

    def __repr__(self):
        return f"{type(self).__name__}({self._dict})"
