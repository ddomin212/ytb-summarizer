import json

import pandas as pd
import streamlit as st

from data_utils.parse_json import write_updated_json


def filters(key_name):
    """
    Initializes filters for the streamlit app dashboard.

    Args:
        key_name (str): The name of the filter. Either "data", "devops" or "web".

    Returns:
        tuple: A tuple of two strings, the first one is the location fiter value,
                the second one is the seniority filter value.
    """
    c1, c2 = st.columns(2)
    with c1:
        misto = st.selectbox(
            "Místo",
            ["Celá ČR", "Praha", "Brno"],
            key=f"loc_{key_name}",
        )
    with c2:
        seniorita = st.selectbox(
            "Senorita",
            ["Všechny", "Junior", "Senior"],
            key=f"pozice_{key_name}",
        )
    return misto, seniorita


def load_data():
    """
    Loads the scraped data from Kaggle API from the generated/scraped/jobs_cz_docs.json file.

    Returns:
        tuple: A tuple of four elements. The first one is a pandas DataFrame,
                the other three are dictionaries containing the various technologies
                related to the dictionary variable name.
    """
    try:
        with open(
            "generated/scraped/jobs_cz_docs.json", "r", encoding="utf-8"
        ) as f:
            json_data = json.load(f)
    except FileNotFoundError:
        write_updated_json()
        with open(
            "generated/scraped/jobs_cz_docs.json", "r", encoding="utf-8"
        ) as f:
            json_data = json.load(f)
    with open("static/devops_technologies.json", "r", encoding="utf-8") as f:
        devops = json.load(f)
    with open("static/data_technologies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("static/web_technologies.json", "r", encoding="utf-8") as f:
        web = json.load(f)
    df = pd.DataFrame(json_data)
    return df, devops, data, web
