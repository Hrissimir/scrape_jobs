from datetime import datetime
from typing import Any, Dict, List, Optional

from bs4 import Tag


class JobResult:

    def __init__(self, tag: Tag):
        if not isinstance(tag, Tag):
            raise TypeError()
        self.tag = tag

    @classmethod
    def keys(cls) -> List[str]:
        return ["utc_datetime", "location", "title", "company", "url"]

    def as_dict(self) -> Dict[str, Any]:
        return dict(zip(self.keys(), self.values()))

    def values(self) -> List[Any]:
        return [getattr(self, key)() for key in self.keys()]

    def get_utc_datetime(self) -> Optional[datetime]:  # pragma: no cover
        raise NotImplementedError()

    def get_location(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    def get_title(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    def get_company(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    def get_url(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()
