import json

import pandas as pd
import streamlit as st


def filters(key_name):
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


def load_data(branch):
    with open(f"jobs_cz_docs.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    with open("devops_technologies.json", "r", encoding="utf-8") as f:
        devops = json.load(f)
    with open("data_technologies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("web_technologies.json", "r", encoding="utf-8") as f:
        web = json.load(f)
    df = pd.DataFrame(json_data)
    return df, devops, data, web
