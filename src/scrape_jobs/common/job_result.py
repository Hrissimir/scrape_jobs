from datetime import datetime
from typing import Optional, List, Dict

from hed_utils.support import log
from hed_utils.support.time_tool import PastTimeParser, convert_to_tz, get_local_tz_name


class JobResult:

    @classmethod
    def get_dict_keys(cls) -> List[str]:
        """Override in child classes"""

        return ["date", "location", "title", "company", "classification", "url"]

    @classmethod
    def parse_post_datetime(cls, value: str, tz_name: Optional[str]) -> datetime:
        local_date = PastTimeParser.parse(value)
        tz_name = tz_name or get_local_tz_name()
        tz_date = convert_to_tz(local_date, tz_name)
        log.debug("parsed job post date [%s] to [%s] (tz_name='%s')", value, tz_date, tz_name)
        return tz_date

    def get_post_date_value(self) -> str:
        raise NotImplementedError()

    def get_post_date(self, tz_name: Optional[str] = None) -> str:
        try:
            post_date_text = self.get_post_date_value()
            post_datetime = self.parse_post_datetime(post_date_text, tz_name)
            return str(post_datetime.date())
        except:
            return "N/A"

    def get_title(self) -> str:
        raise NotImplementedError()

    def get_location(self) -> str:
        raise NotImplementedError()

    def get_company(self) -> str:
        raise NotImplementedError()

    def get_classification(self) -> str:
        raise NotImplementedError()

    def get_url(self) -> str:
        raise NotImplementedError()

    def as_dict(self, tz_name: Optional[str] = None) -> Dict[str, str]:
        """Override in child classes"""

        return dict(date=self.get_post_date(tz_name),
                    location=self.get_location(),
                    title=self.get_title(),
                    company=self.get_company(),
                    classification=self.get_classification(),
                    url=self.get_url())
