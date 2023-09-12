import json
from functools import partial

import pandas as pd
import streamlit as st
import altair as alt

from data_utils.parse_jobs import filter_dataframe_tech
from data_utils.settings import DATA_REGEX, DEVOPS_REGEX, WEB_REGEX, CLOUD_REGEX

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

def select_job_position(selected, df, misto, devops, data, web):
    """filters the dataframe according to the selected job position

    Args:
        selected: the job position selected
        df: dataframe with job postings
        misto: selected location
        devops: dictionary of devops technologies
        data: dictionary of data technologies
        web: dictionary of web technologies

    Returns:
        filtered dataframe
    """
    partial_filter = partial(filter_dataframe_tech, df=df, misto=misto)
    if selected == "DevOps":
        tech_data = partial_filter(devops, DEVOPS_REGEX)
    if selected == "Web":
        tech_data = partial_filter({**web, **devops}, WEB_REGEX)
    if selected == "Data":
        tech_data = partial_filter({**data, **devops}, DATA_REGEX)
    if selected == "Cloud":
        tech_data = partial_filter({**web, **devops}, DEVOPS_REGEX)
    return tech_data

def plot_chart(tech_data):
    """create an altair chart showing the number of jobs for each technology

    Args:
        tech_data: dataframe including the number of jobs for each technology

    Returns:
        altar chart
    """
    alt.data_transformers.enable("default", max_rows=None)
    alt.renderers.set_embed_options(dpi=300)
    c = (
        alt.Chart(tech_data[tech_data.Count > 2])
        .mark_bar()
        .encode(
            x="Count:Q",
            y=alt.Y("Tech:N", sort="-x"),  # Sort the bars in descending order
            tooltip=["Tech", "Count", "Branch"],
            color="Branch:N",
        )
    )
    return c

def detail(loc_data, pay_data):
    """plot the detailed info on the pay and number of jobs

    Args:
        loc_data: number of jobs in all locations
        pay_data: median pay in a given location
    """
    c3, c4 = st.columns(2)
    with c3:
        st.dataframe(loc_data, use_container_width=True, height=200)
    with c4:
        st.metric(label="Median Pay", value=str(pay_data) + " Kč/měsíc")
        st.metric(label="Number of jobs", value=str(sum(loc_data.values.tolist())))