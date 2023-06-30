import os

import altair as alt
import streamlit as st
from streamlit_option_menu import option_menu

# from data_utils.agent import init_agent, query
from data_utils.date_check import check_date
from data_utils.parse_jobs import get_locations, get_pay, get_tech
from data_utils.st_utils import filters, load_data
from utils.regexes import cloud_r, data_r, devops_r, web_r

if os.getenv("MODE") != "production":
    from dotenv import load_dotenv

    load_dotenv()
date = os.getenv("START_DATE")
date = check_date(date)
os.environ["START_DATE"] = date
print(os.getenv("START_DATE"))

st.header("Select your desired field of work:")
selected = option_menu(
    None,
    ["Data", "Web", "DevOps", "Cloud"],
    icons=["clipboard-data-fill", "browser-chrome", "infinity", "cloud"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)


misto, seniorita = filters(selected)
df, devops, data, web = load_data()

if selected == "DevOps":
    df = df[df.title.str.contains(devops_r)]
    TECH_DATA = get_tech(df, misto, devops)
if selected == "Web":
    df = df[df.title.str.contains(web_r)]
    TECH_DATA = get_tech(df, misto, {**web, **devops})
if selected == "Data":
    df = df[df.title.str.contains(data_r)]
    TECH_DATA = get_tech(df, misto, {**data, **devops})
if selected == "Cloud":
    df = df[df.title.str.contains(cloud_r)]
    TECH_DATA = get_tech(df, misto, {**web, **devops})

loc_data = get_locations(df, seniorita)
pay_data = get_pay(df, seniorita)

alt.data_transformers.enable("default", max_rows=None)
alt.renderers.set_embed_options(dpi=300)
c = (
    alt.Chart(TECH_DATA[TECH_DATA.Count > 2])
    .mark_bar()
    .encode(
        x="Count:Q",
        y=alt.Y("Tech:N", sort="-x"),  # Sort the bars in descending order
        tooltip=["Tech", "Count", "Branch"],
        color="Branch:N",
    )
)

st.divider()

c3, c4 = st.columns(2)
with c3:
    st.dataframe(loc_data, use_container_width=True, height=200)
with c4:
    st.metric(label="Median Pay", value=str(pay_data) + " Kč/měsíc")
    st.metric(label="Number of jobs", value=str(sum(loc_data.values.tolist())))

chart = st.altair_chart(c, theme="streamlit", use_container_width=True)
