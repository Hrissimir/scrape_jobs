from configparser import ConfigParser
from pathlib import Path
from tempfile import TemporaryDirectory

from scrape_jobs.common import config


def test_write_sample():
    with TemporaryDirectory() as tmp_dir:
        config.write_sample(tmp_dir)
        sample_file = Path(tmp_dir).joinpath(config.DEFAULT_FILENAME)
        assert sample_file.read_text(encoding="utf-8") == config.SAMPLE_FILEPATH.read_text(encoding="utf-8")


def test_parse_sheets_config():
    section = dict(upload_spreadsheet_name="test spreadsheet",
                   upload_spreadsheet_json=r"path/to/secrets.json",
                   upload_worksheet_index="1",
                   upload_worksheet_urls_column_index="2")
    cfg = ConfigParser()
    cfg["section"] = section
    sheets_config = config.parse_sheets_config(cfg, "section")
    assert sheets_config.spreadsheet_name == "test spreadsheet"
    assert sheets_config.json_filepath == r"path/to/secrets.json"
    assert sheets_config.worksheet_index == 1
    assert sheets_config.urls_column_index == 2


def test_parse_time_config():
    section = dict(timezone="Australia/Sydney",
                   max_post_age_days="5",
                   scraped_timestamp_format="%Y-%m-%d %H:%M",
                   posted_timestamp_format="%Y-%m-%d %H:00")
    cfg = ConfigParser(interpolation=None)
    cfg["section"] = section

    time_config = config.parse_time_config(cfg, "section")
    assert time_config.timezone == "Australia/Sydney"
    assert time_config.max_post_age_days == 5
    assert time_config.scraped_timestamp_format == "%Y-%m-%d %H:%M"
    assert time_config.posted_timestamp_format == "%Y-%m-%d %H:00"
