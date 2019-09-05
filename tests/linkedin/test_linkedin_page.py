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

        expected_jobs_text = (
            """[
            {'utc_datetime': datetime.datetime(2019, 8, 16, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, Bulgaria', 'title': 'Shumen, Bulgaria', 'company': 'Diavena ltd', 'url': 'https://bg.linkedin.com/jobs/view/export-manager-at-diavena-ltd-1414285071'}, 
            {'utc_datetime': datetime.datetime(2019, 8, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, Bulgaria', 'title': 'Shumen, Bulgaria', 'company': 'Diavena ltd', 'url': 'https://bg.linkedin.com/jobs/view/production-manager-at-diavena-ltd-1444224357'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Transport Directorate FIFA World Cup Russia 2018', 'url': 'https://bg.linkedin.com/jobs/view/%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82-at-transport-directorate-fifa-world-cup-russia-2018-1284068797'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Leona', 'url': 'https://bg.linkedin.com/jobs/view/%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82-at-leona-1283549484'}, 
            {'utc_datetime': datetime.datetime(2019, 7, 2, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'гарант', 'url': 'https://bg.linkedin.com/jobs/view/%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA-%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%81%D1%82%D0%B2%D0%BE-%D0%B8-%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0-at-%D0%B3%D0%B0%D1%80%D0%B0%D0%BD%D1%82-1360660760'}, 
            {'utc_datetime': datetime.datetime(2019, 6, 19, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'АО МСО "Надежда"', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D0%BD%D1%82-at-%D0%B0%D0%BE-%D0%BC%D1%81%D0%BE-%D0%BD%D0%B0%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-1346337332'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Наша Виктория', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%87-%D0%B7%D0%B0%D0%BA%D1%83%D1%81%D0%BA%D0%B8-%D0%B8-%D0%BD%D0%B0%D0%BF%D0%B8%D1%82%D0%BA%D0%B8-at-%D0%BD%D0%B0%D1%88%D0%B0-%D0%B2%D0%B8%D0%BA%D1%82%D0%BE%D1%80%D0%B8%D1%8F-1283573343'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Нова Пошта', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BA%D0%BE%D1%84%D1%80%D0%B0%D0%B6%D0%B8%D1%81%D1%82-at-%D0%BD%D0%BE%D0%B2%D0%B0-%D0%BF%D0%BE%D1%88%D1%82%D0%B0-1283571355'}, 
            {'utc_datetime': datetime.datetime(2018, 11, 23, 0, 0, tzinfo=<UTC>), 'location': 'Tsarev Brod, BG', 'title': 'Tsarev Brod, BG', 'company': 'New York Pizza', 'url': 'https://bg.linkedin.com/jobs/view/scooter-bezorger-at-new-york-pizza-981379824'}, 
            {'utc_datetime': datetime.datetime(2019, 8, 21, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'вилла Панорама', 'url': 'https://bg.linkedin.com/jobs/view/%D0%B3%D0%BE%D1%82%D0%B2%D0%B0%D1%87-at-%D0%B2%D0%B8%D0%BB%D0%BB%D0%B0-%D0%BF%D0%B0%D0%BD%D0%BE%D1%80%D0%B0%D0%BC%D0%B0-1457749338'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Leona', 'url': 'https://bg.linkedin.com/jobs/view/%D1%81%D1%82%D0%B0%D1%80%D1%88%D0%B8-%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82-at-leona-1283300563'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Transport Directorate FIFA World Cup Russia 2018', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BF%D1%80%D0%BE%D1%84%D0%B5%D1%81%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D0%B5%D0%BD-%D0%BA%D0%BE%D0%BD%D1%81%D1%83%D0%BB%D1%82%D0%B0%D0%BD%D1%82-at-transport-directorate-fifa-world-cup-russia-2018-1283790394'}, 
            {'utc_datetime': datetime.datetime(2018, 11, 23, 0, 0, tzinfo=<UTC>), 'location': 'Tsarev Brod, BG', 'title': 'Tsarev Brod, BG', 'company': 'New York Pizza', 'url': 'https://bg.linkedin.com/jobs/view/fietskoerier-at-new-york-pizza-981379823'}, 
            {'utc_datetime': datetime.datetime(2019, 7, 22, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': '"БАКХУС - 4 КЛОН КАСПИЧАН" ООД', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D0%BD%D1%82-at-%D0%B1%D0%B0%D0%BA%D1%85%D1%83%D1%81-4-%D0%BA%D0%BB%D0%BE%D0%BD-%D0%BA%D0%B0%D1%81%D0%BF%D0%B8%D1%87%D0%B0%D0%BD-%D0%BE%D0%BE%D0%B4-1435463749'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 27, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Leona', 'url': 'https://bg.linkedin.com/jobs/view/%D1%82%D1%80%D1%83%D0%B4%D0%BE%D0%B2-%D0%BF%D0%BE%D1%81%D1%80%D0%B5%D0%B4%D0%BD%D0%B8%D0%BA-at-leona-1284409424'}, 
            {'utc_datetime': datetime.datetime(2019, 6, 19, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'АО МСО "Надежда"', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BE%D0%B1%D1%89-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BD%D0%B8%D0%BA-at-%D0%B0%D0%BE-%D0%BC%D1%81%D0%BE-%D0%BD%D0%B0%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0-1335044105'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Transport Directorate FIFA World Cup Russia 2018', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BC%D0%BB%D0%B0%D0%B4%D1%88%D0%B8-%D0%B5%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%82-at-transport-directorate-fifa-world-cup-russia-2018-1283773363'}, 
            {'utc_datetime': datetime.datetime(2019, 7, 16, 0, 0, tzinfo=<UTC>), 'location': 'Tsarev Brod, BG', 'title': 'Tsarev Brod, BG', 'company': 'New York Pizza', 'url': 'https://bg.linkedin.com/jobs/view/pizza-bakker-at-new-york-pizza-1381081066'}, 
            {'utc_datetime': datetime.datetime(2019, 5, 29, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'СРЕДНО УЧИЛИЩЕ "П.ВОЛОВ" Училище', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D0%BD%D0%B8%D0%BA-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D1%80-%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D0%BE-%D1%81%D1%82%D0%BE%D0%BF%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%82%D0%B0-%D0%B4%D0%B5%D0%B9%D0%BD%D0%BE%D1%81%D1%82-at-%D1%81%D1%80%D0%B5%D0%B4%D0%BD%D0%BE-%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%B5-%D0%BF-%D0%B2%D0%BE%D0%BB%D0%BE%D0%B2-%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%B5-1298958173'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'Transport Directorate FIFA World Cup Russia 2018', 'url': 'https://bg.linkedin.com/jobs/view/%D0%B3%D0%BB%D0%B0%D0%B2%D0%B5%D0%BD-%D0%B5%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%82-at-transport-directorate-fifa-world-cup-russia-2018-1283377308'}, 
            {'utc_datetime': datetime.datetime(2019, 7, 9, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'ОБЩИНА КАСПИЧАН община', 'url': 'https://bg.linkedin.com/jobs/view/%D1%82%D1%80%D1%83%D0%B4%D0%BE%D0%B2-%D0%BF%D0%BE%D1%81%D1%80%D0%B5%D0%B4%D0%BD%D0%B8%D0%BA-at-%D0%BE%D0%B1%D1%89%D0%B8%D0%BD%D0%B0-%D0%BA%D0%B0%D1%81%D0%BF%D0%B8%D1%87%D0%B0%D0%BD-%D0%BE%D0%B1%D1%89%D0%B8%D0%BD%D0%B0-1409895678'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 27, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'ЦЕНТЪР ЗА СПЕЦИАЛНА ОБРАЗОВАТЕЛНА ПОДКРЕПА Училище', 'url': 'https://bg.linkedin.com/jobs/view/%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D0%BD%D0%B8%D0%BA-%D0%BD%D0%B0-%D1%83%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8F-at-%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80-%D0%B7%D0%B0-%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%BD%D0%B0-%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%BD%D0%B0-%D0%BF%D0%BE%D0%B4%D0%BA%D1%80%D0%B5%D0%BF%D0%B0-%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%B5-1284247248'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'ОСНОВНО УЧИЛИЩЕ "ХРИСТО СМИРНЕНСКИ" Училище', 'url': 'https://bg.linkedin.com/jobs/view/%D1%83%D1%87%D0%B8%D1%82%D0%B5%D0%BB-%D0%BD%D0%B0%D1%87%D0%B0%D0%BB%D0%B5%D0%BD-%D0%B5%D1%82%D0%B0%D0%BF-%D0%BD%D0%B0-%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE%D1%82%D0%BE-%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-i-iv-%D0%BA%D0%BB%D0%B0%D1%81-at-%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%BE-%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%B5-%D1%85%D1%80%D0%B8%D1%81%D1%82%D0%BE-%D1%81%D0%BC%D0%B8%D1%80%D0%BD%D0%B5%D0%BD%D1%81%D0%BA%D0%B8-%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%B5-1283769842'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'ДЕТСКА ГРАДИНА "ЩАСТЛИВО ДЕТСТВО" Детска градина', 'url': 'https://bg.linkedin.com/jobs/view/%D1%83%D1%87%D0%B8%D1%82%D0%B5%D0%BB-%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0-%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%BD%D0%B0-at-%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0-%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%BD%D0%B0-%D1%89%D0%B0%D1%81%D1%82%D0%BB%D0%B8%D0%B2%D0%BE-%D0%B4%D0%B5%D1%82%D1%81%D1%82%D0%B2%D0%BE-%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0-%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%BD%D0%B0-1283733011'}, 
            {'utc_datetime': datetime.datetime(2019, 4, 26, 0, 0, tzinfo=<UTC>), 'location': 'Shumen, BG', 'title': 'Shumen, BG', 'company': 'ЛФС ЕООД', 'url': 'https://bg.linkedin.com/jobs/view/%D0%B3%D0%BE%D1%82%D0%B2%D0%B0%D1%87-at-%D0%BB%D1%84%D1%81-%D0%B5%D0%BE%D0%BE%D0%B4-1283703784'}
            ]""")
        actual_jobs = [j.as_dict() for j in jobs.get_visible_results()]
        actual_jobs_text = repr(actual_jobs)

        self.assertEqual(expected_jobs_text, actual_jobs_text)
