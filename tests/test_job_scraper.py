import os
from datetime import datetime

import pandas as pd

from data_utils.parse import (
    filter_dataframe_tech,
    get_locations,
    get_pay,
    get_tech,
    select_job_position,
)
from data_utils.scrape import scrape_new_data, load_data
from data_utils.settings import (
    CLOUD_REGEX,
    DATA_REGEX,
    DEVOPS_REGEX,
    WEB_REGEX,
)


def test_scrape_new_data():
    os.environ["START_DATE"] = "2021-09-17"
    str_today = datetime.today().strftime("%Y-%m-%d")
    scrape_new_data()
    assert os.getenv("START_DATE") == str_today
    scrape_new_data()
    assert os.getenv("START_DATE") == str_today


def test_load_data():
    df, devops, data, web = load_data()
    assert isinstance(df, pd.DataFrame)
    assert isinstance(devops, dict)
    assert isinstance(data, dict)
    assert isinstance(web, dict)
    assert df.shape == (2688, 7)


def test_select_job_position_data(mocked_data):
    _, devops, data, web = load_data()
    df = select_job_position("Data", mocked_data, "Celá ČR", devops, data, web)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (24, 3)
    assert df["Count"].sum() == 109


def test_filter_dataframe_tech(mocked_data, data, devops):
    df = filter_dataframe_tech(
        df=mocked_data,
        misto="Celá ČR",
        tech_dict={**data, **devops},
        regex=DATA_REGEX,
    )
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (24, 3)
    assert df["Count"].sum() == 109


def test_get_pay(mocked_data):
    median_pay = get_pay(mocked_data, "Celá ČR", "Všechny")
    assert median_pay == 70000


def test_get_locations(mocked_data):
    s = get_locations(mocked_data, "Celá ČR", "Všechny")
    assert isinstance(s, pd.Series)
    assert s.shape == (18,)


def test_get_tech(mocked_data, data, devops):
    df = get_tech(mocked_data, "Celá ČR", {**data, **devops})
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (84, 3)
