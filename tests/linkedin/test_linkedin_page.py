from pathlib import Path
from unittest import TestCase
from urllib.parse import urljoin

from hed_utils.selenium import driver

from scrape_jobs.sites.linkedin_com.linkedin_results_context import LinkedinResultsContext
from scrape_jobs.sites.linkedin_com.linkedin_search_context import LinkedinSearchContext
from scrape_jobs.sites.linkedin_com.linkedin_search_section import LinkedinSearchSection


class TestLinkedinStatic(TestCase):
    JOB_RESULT_HTML = "job_result.html"
    LINKEDIN_RESULTS_HTML = "linkedin_results.html"
    LINKEDIN_SEARCH_HTML = "linkedin_search.html"

    @classmethod
    def setUpClass(cls) -> None:
        driver.start_chrome()

    @classmethod
    def tearDownClass(cls) -> None:
        driver.quit()

    @classmethod
    def load_html(cls, file_name):
        file_path = str(Path(__file__).parent.joinpath(file_name))
        file_url = urljoin("file:///", file_path)
        driver.get(file_url, wait_for_url_changes=False, wait_for_page_load=True)

    def setUp(self) -> None:
        self.page = LinkedinSearchContext()
        self.maxDiff = None

    def tearDown(self) -> None:
        self.page = None

    def test_can_find_search_bar_elements(self):
        self.load_html(self.LINKEDIN_RESULTS_HTML)
        bar: LinkedinSearchSection = self.page.JOBS_SEARCH_BAR

        self.assertTrue(bar.is_visible())
        self.assertTrue(driver.is_visible(bar.keywords_input_locator))
        self.assertTrue(driver.is_visible(bar.location_input_locator))
        self.assertTrue(driver.is_visible(bar.search_button_locator))

    def test_can_find_search_form_elements(self):
        self.load_html(self.LINKEDIN_SEARCH_HTML)
        form: LinkedinSearchSection = self.page.JOBS_SEARCH_FORM

        self.assertTrue(form.is_visible())
        self.assertTrue(driver.is_visible(form.keywords_input_locator))
        self.assertTrue(driver.is_visible(form.location_input_locator))
        self.assertTrue(driver.is_visible(form.search_button_locator))

    def test_can_find_search_results_elements(self):
        self.load_html(self.LINKEDIN_RESULTS_HTML)
        jobs: LinkedinResultsContext = self.page.JOBS_RESULTS

        self.assertTrue(jobs.is_visible())
        self.assertTrue(len(jobs.elements()) == 25)

        expected_jobs_text = "[{'utc_datetime': datetime.datetime(2019, 8, 28, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Automation QA Engineer (Virtualization Backup)', 'company': 'Acronis', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-engineer-virtualization-backup-at-acronis-1432803744'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 9, 3, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Engineer', 'company': 'Takeaway.com', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-at-takeaway-com-1442570534'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 27, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, Sofia City Province, Bulgaria', 'title': 'Senior QA Automation Engineer', 'company': 'i:FAO Group GmbH', 'url': 'https://bg.linkedin.com/jobs/view/senior-qa-automation-engineer-at-i-fao-group-gmbh-1427710012'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 13, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Automation QA Engineer', 'company': 'Nemetschek Bulgaria', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-engineer-at-nemetschek-bulgaria-1429942101'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 28, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Automation QA Engineer', 'company': 'СИРМА СОЛЮШЪНС АД', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-engineer-at-%D1%81%D0%B8%D1%80%D0%BC%D0%B0-%D1%81%D0%BE%D0%BB%D1%8E%D1%88%D1%8A%D0%BD%D1%81-%D0%B0%D0%B4-1463678372'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 6, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Automation QA Engineer', 'company': 'Programista; JSC', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-engineer-at-programista-jsc-1439531050'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 6, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'AUTOMATION QA ENGINEER', 'company': 'Talent Hunter Treinamentos', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-engineer-at-talent-hunter-treinamentos-1415839162'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 14, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Software QA Automation Engineer', 'company': 'Secure Group', 'url': 'https://bg.linkedin.com/jobs/view/software-qa-automation-engineer-at-secure-group-1431957398'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 23, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Automation QA', 'company': 'SBTech', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-at-sbtech-1453476034'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 7, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Automation QA Engineer', 'company': 'Strypes', 'url': 'https://bg.linkedin.com/jobs/view/automation-qa-engineer-at-strypes-1418558860'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 21, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Engineer (Mobile Applications)', 'company': 'Receipt Bank', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-mobile-applications-at-receipt-bank-1447345058'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 8, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Engineer (Manual Testing)', 'company': 'Musala Soft', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-manual-testing-at-musala-soft-1420753708'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 9, 4, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Tester', 'company': 'Luxoft', 'url': 'https://bg.linkedin.com/jobs/view/qa-tester-at-luxoft-1448561640'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 20, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Mid-Level Automation QA Engineer', 'company': 'Astrea Recruitment', 'url': 'https://bg.linkedin.com/jobs/view/mid-level-automation-qa-engineer-at-astrea-recruitment-1445492054'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 14, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Engineer', 'company': 'Catenate', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-at-catenate-1431698722'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 30, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Engineer', 'company': 'The Coca-Cola Company', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-at-the-coca-cola-company-1476011078'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 9, 5, 0, 0, tzinfo=<UTC>), 'location': 'Sofia City, Bulgaria', 'title': 'QA Engineer', 'company': 'Nuvolo', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-at-nuvolo-1448593500'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 26, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, Sofia City Province, Bulgaria', 'title': 'Senior QA Automation Engineer', 'company': 'Digitise Labs Bulgaria', 'url': 'https://bg.linkedin.com/jobs/view/senior-qa-automation-engineer-at-digitise-labs-bulgaria-1335156082'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 26, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Engineer', 'company': 'Accedia', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-at-accedia-1458038968'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 23, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Automation Engineer', 'company': 'Progress', 'url': 'https://bg.linkedin.com/jobs/view/qa-automation-engineer-at-progress-1398103773'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 9, 3, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, Sofia City Province, Bulgaria', 'title': 'Quality Assurance Engineer', 'company': 'HyperScience', 'url': 'https://bg.linkedin.com/jobs/view/quality-assurance-engineer-at-hyperscience-1448505009'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 10, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Test Automation Engineer (StarsWeb)', 'company': 'The Stars Group', 'url': 'https://bg.linkedin.com/jobs/view/test-automation-engineer-starsweb-at-the-stars-group-1448540834'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 28, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA ENGINEER', 'company': 'BULWORK', 'url': 'https://bg.linkedin.com/jobs/view/qa-engineer-at-bulwork-1463510319'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 19, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'Test Automation Engineer', 'company': 'Fadata Group', 'url': 'https://bg.linkedin.com/jobs/view/test-automation-engineer-at-fadata-group-1442742119'}, " \
                             "{'utc_datetime': datetime.datetime(2019, 8, 22, 0, 0, tzinfo=<UTC>), 'location': 'Sofia, BG', 'title': 'QA Specialist | New R&D Center', 'company': 'JTR', 'url': 'https://bg.linkedin.com/jobs/view/qa-specialist-new-r-d-center-at-jtr-1450820005'}]"

        actual_jobs = [j.as_dict() for j in jobs.get_visible_results()]
        actual_jobs_text = repr(actual_jobs)

        self.assertEqual(expected_jobs_text, actual_jobs_text)
