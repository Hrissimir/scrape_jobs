"""This module wraps interaction with  dicts containing jobs data"""

from datetime import datetime, timedelta

from hed_utils.support.time_tool import PastTimeParser, convert_to_tz, get_local_tz_name, get_local_datetime

KEYS = ["date", "location", "title", "company", "classification", "url"]


def parse_posted_datetime(posted: str, tz_name=None) -> datetime:
    tz_name = tz_name or get_local_tz_name()
    posted_datetime_in_local_tz = PastTimeParser.parse(posted)
    posted_datetime_in_target_tz = convert_to_tz(posted_datetime_in_local_tz, tz_name)
    return posted_datetime_in_target_tz


def new_post() -> dict:
    return dict(date="NO_DATE",
                location="NO_LOCATION",
                title="NO_TITLE",
                company="NO_COMPANY",
                classification="NO_CLASSIFICATION",
                url="NO_URL",
                salary="NO_SALARY")


def set_date(post, date: str):
    post["date"] = date


def get_date(post) -> str:
    return post.get("date", "NO_DATE")


def set_location(post, location: str):
    post["location"] = location


def get_location(post) -> str:
    return post.get("location", "NO_LOCATION")


def set_title(post, title: str):
    post["title"] = title


def get_title(post) -> str:
    return post.get("title", "NO_TITLE")


def set_company(post, company: str):
    post["company"] = company


def get_company(post) -> str:
    return post.get("company", "NO_COMPANY")


def set_classification(post, classification):
    post["classification"] = classification


def get_classification(post) -> str:
    return post.get("classification", "NO_CLASSIFICATION")


def set_url(post, url: str):
    post["url"] = url


def get_url(post) -> str:
    return post.get("url", "NO_URL")


def set_salary(post, salary):
    post["salary"] = salary


def get_salary(post) -> str:
    return post.get("salary", "NO_SALARY")


def age_predicate(*, n_days: int, tz_name: str = None):
    """Returns a predicate function that checks if the passed job is younger than past n_days"""

    tz_name = tz_name or get_local_tz_name()

    datetime_in_local_tz = get_local_datetime()
    limit_datetime_in_local_tz = datetime_in_local_tz - timedelta(days=n_days)
    limit_datetime_in_target_tz = convert_to_tz(limit_datetime_in_local_tz, tz_name)
    limit_date_in_target_tz = limit_datetime_in_target_tz.date()

    def should_keep(job) -> bool:
        try:
            posted = get_date(job)
            job_date_in_target_tz = parse_posted_datetime(posted, tz_name).date()
            return limit_date_in_target_tz < job_date_in_target_tz
        except:
            return False

    return should_keep
