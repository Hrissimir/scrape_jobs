from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from hed_utils.support import time_tool


class ResultPredicate(ABC):

    @abstractmethod
    def __call__(self, data: dict) -> bool:  # pragma: no cover
        pass


class MaxDaysAge(ResultPredicate):
    def __init__(self, days: int):
        if not isinstance(days, int):
            raise TypeError()
        if days <= 0:
            raise ValueError()

        self.mark_date = (time_tool.utc_moment() - timedelta(days=days)).date()

    def __call__(self, data: dict) -> bool:
        post_utc_datetime: Optional[datetime] = data.get("utc_datetime", None)
        if post_utc_datetime:
            return post_utc_datetime.date() >= self.mark_date
        else:
            return False
