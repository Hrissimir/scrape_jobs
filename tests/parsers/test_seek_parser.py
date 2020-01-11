from pathlib import Path

from scrape_jobs.parsers import seek_parser

RESULTS_FILE = Path(__file__).parent.joinpath("static").joinpath("seek_results.html")
RESULTS_SOURCE = RESULTS_FILE.read_text()


def test_get_tags():
    soups = seek_parser.get_tags(RESULTS_SOURCE)
    assert len(soups) == 22


def test_get_title():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    title = seek_parser.get_title(tag)
    assert title == "Senior Performance Engineer"


def test_get_company():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    company = seek_parser.get_company(tag)
    assert company == "Cognizant Technology Solutions Australia Pty Ltd"


def test_get_location():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    location = seek_parser.get_location(tag)
    assert location == "Sydney"


def test_get_area():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    area = seek_parser.get_area(tag)
    assert area == "CBD, Inner West & Eastern Suburbs"


def test_get_salary():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    salary = seek_parser.get_salary(tag)
    assert salary == "$80,000 - $119,999"


def test_get_classification():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    classification = seek_parser.get_classification(tag)
    assert classification == "Information & Communication Technology"


def test_get_sub_classification():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    sub_classification = seek_parser.get_sub_classification(tag)
    assert sub_classification == "Testing & Quality Assurance"


def test_get_posted():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[2]
    posted = seek_parser.get_posted(tag)
    assert posted == "6d ago"


def test_get_url():
    tag = seek_parser.get_tags(RESULTS_SOURCE)[0]
    url = seek_parser.get_url(tag)
    assert url == "https://seek.com.au/job/40624451"


def test_parse_jobs():
    expected_jobs = [
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Cognizant Technology Solutions Australia Pty Ltd",
            "location": "Sydney",
            "posted": None,
            "salary": "$80,000 - $119,999",
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Performance Engineer",
            "url": "https://seek.com.au/job/40624451"
        },
        {
            "area": "North Shore & Northern Beaches",
            "classification": "Information & Communication Technology",
            "company": "Vocus",
            "location": "Sydney",
            "posted": None,
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Functional Test Lead - HCM Project",
            "url": "https://seek.com.au/job/40688932"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Attribute Group",
            "location": "Sydney",
            "posted": "6d ago",
            "salary": "Excellent contract and permanent opportunities",
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Test Automation Engineer",
            "url": "https://seek.com.au/job/40658311"
        },
        {
            "area": "Parramatta & Western Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Link Group",
            "location": "Sydney",
            "posted": "1d ago",
            "salary": None,
            "sub_classification": "Business/Systems Analysts",
            "title": "Senior Automation Test Engineer",
            "url": "https://seek.com.au/job/40709214"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "PRA",
            "location": "Sydney",
            "posted": "4d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Automation Test Engineer",
            "url": "https://seek.com.au/job/40680338"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Attribute Group",
            "location": "Sydney",
            "posted": "5d ago",
            "salary": "Top $$$",
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Test Automation Engineer - (Contract)",
            "url": "https://seek.com.au/job/40661647"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Standards Australia Ltd",
            "location": "Sydney",
            "posted": "5d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Automation Test Analyst",
            "url": "https://seek.com.au/job/40664426"
        },
        {
            "area": None,
            "classification": "Information & Communication Technology",
            "company": "Revolution IT",
            "location": "Sydney",
            "posted": "5d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Automation Engineer (API Testing)",
            "url": "https://seek.com.au/job/40666918"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Harvey Nash",
            "location": "Sydney",
            "posted": "2d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Test Automation Engineer (Java) - Permanent role",
            "url": "https://seek.com.au/job/40698001"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Ambition",
            "location": "Sydney",
            "posted": "2d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Automation Test Analyst",
            "url": "https://seek.com.au/job/40695825"
        },
        {
            "area": None,
            "classification": "Information & Communication Technology",
            "company": "Sirius Technology Sydney part of Sirius People Pty Ltd",
            "location": "Sydney",
            "posted": "10d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Test Automation Engineer",
            "url": "https://seek.com.au/job/40642333"
        },
        {
            "area": None,
            "classification": "Information & Communication Technology",
            "company": "Attribute Group",
            "location": "Sydney",
            "posted": "6d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Multiple Senior Automation Engineer - API focus",
            "url": "https://seek.com.au/job/40660799"
        },
        {
            "area": None,
            "classification": "Information & Communication Technology",
            "company": "Attribute Testing",
            "location": "Sydney",
            "posted": "6d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Multiple Senior Automation Engineer - API focus",
            "url": "https://seek.com.au/job/40660807"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Fyndr Group",
            "location": "Sydney",
            "posted": "1d ago",
            "salary": "$120k + super",
            "sub_classification": "Testing & Quality Assurance",
            "title": "JavaScript Automation Engineer",
            "url": "https://seek.com.au/job/40706630"
        },
        {
            "area": None,
            "classification": "Information & Communication Technology",
            "company": "Opus Recruitment Solutions",
            "location": "Sydney",
            "posted": "10d ago",
            "salary": "$600 - $750 per day",
            "sub_classification": "Testing & Quality Assurance",
            "title": "Automation Test Engineer",
            "url": "https://seek.com.au/job/40643351"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Needus",
            "location": "Sydney",
            "posted": "11d ago",
            "salary": "$130 - $145K base",
            "sub_classification": "Testing & Quality Assurance",
            "title": "Software Engineer in Test (Mobile Team), $130 - $145K base, Sydney "
                     "CBD Location",
            "url": "https://seek.com.au/job/40639536"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "TL Consulting Group",
            "location": "Sydney",
            "posted": "10d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Test Automation Engineer",
            "url": "https://seek.com.au/job/40641672"
        },
        {
            "area": "Parramatta & Western Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Revolution IT",
            "location": "Sydney",
            "posted": "10h ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "TOSCA Automation",
            "url": "https://seek.com.au/job/40711283"
        },
        {
            "area": None,
            "classification": "Information & Communication Technology",
            "company": "Aurec",
            "location": "Sydney",
            "posted": "5d ago",
            "salary": None,
            "sub_classification": "Developers/Programmers",
            "title": "QA Automation Engineer",
            "url": "https://seek.com.au/job/40668267"
        },
        {
            "area": "Ryde & Macquarie Park",
            "classification": "Information & Communication Technology",
            "company": "Foxtel Management Pty Limited",
            "location": "Sydney",
            "posted": "5d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Automation Test Analyst",
            "url": "https://seek.com.au/job/40668833"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Harvey Nash",
            "location": "Sydney",
            "posted": "9d ago",
            "salary": None,
            "sub_classification": "Testing & Quality Assurance",
            "title": "Senior Test Automation Engineer (Java) - Permanent role",
            "url": "https://seek.com.au/job/40645497"
        },
        {
            "area": "CBD, Inner West & Eastern Suburbs",
            "classification": "Information & Communication Technology",
            "company": "Evolution Recruitment Solutions Pty Ltd",
            "location": "Sydney",
            "posted": "6d ago",
            "salary": "$$$ Leading daily rates $$$",
            "sub_classification": "Testing & Quality Assurance",
            "title": "Automation Tester",
            "url": "https://seek.com.au/job/40642557"
        }
    ]

    actual_jobs = seek_parser.parse_jobs(RESULTS_SOURCE)
    assert expected_jobs == actual_jobs
    print()
    print(seek_parser.format_jobs(actual_jobs))
