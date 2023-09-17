import json
import os
import shutil

import pandas as pd
import pytest
from dotenv import load_dotenv

load_dotenv()

if os.path.isdir("generated/dataset"):
    shutil.rmtree("generated/dataset")

if os.path.isdir("generated/kernel"):
    shutil.rmtree("generated/kernel")

if os.path.isdir("generated/output"):
    shutil.rmtree("generated/output")


@pytest.fixture()
def mocked_data():
    with open("static/mocked_jobs.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        return pd.DataFrame(json_data)


@pytest.fixture()
def devops():
    with open("static/devops_technologies.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data


@pytest.fixture()
def data():
    with open("static/data_technologies.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data
