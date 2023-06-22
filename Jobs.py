import altair as alt
import streamlit as st
from streamlit_card import card
from streamlit_option_menu import option_menu

from data_utils.parse_jobs import get_locations, get_pay, get_tech
from data_utils.st_utils import filters, load_data

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
df, devops, data, web = load_data(selected)

if selected == "DevOps":
    df = df[
        df.title.str.contains(
            "(?i)devops|mlops|jenkins|kubernetes|docker|dataops|ops|gitlab|ansible|terraform|aws|azure|gcp|cloud"
        )
    ]
    tech_data = get_tech(df, misto, devops)
if selected == "Web":
    df = df[
        df.title.str.contains(
            """(?i)frontend|backend|fullstack|full stack|vue|react|angular|svelte|web developer|webdev|web dev
            |webdesign|web design|webdesigner|web designer|webmaster|web master|webmaster
            |web master|django|spring|flask|node|php|wordpress|drupal|laravel|symfony|ruby|rails|html|css|javascript|typescript|developer|lamp|mean|mern|vývojář|webový"""
        )
    ]
    tech_data = get_tech(df, misto, {**web, **devops})
if selected == "Data":
    df = df[
        df.title.str.contains(
            "(?i)data|database|databáze|databaze|sql|nosql|etl|dataops|data ops|dataops|data ops|data engineer|data scientist|data analyst|bi|buissness|analytik|vědec|umělá inteligence|umělou inteligenci| ai |machine learning| ml |big data|strojové učení"
        )
    ]
    tech_data = get_tech(df, misto, {**data, **devops})
if selected == "Cloud":
    df = df[df.title.str.contains("(?i)cloud|azure|aws|gcp|google|cloudový")]
    tech_data = get_tech(df, misto, {**web, **devops})

loc_data = get_locations(df, misto, seniorita)
pay_data = get_pay(df, misto, seniorita)

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
st.divider()
c3, c4 = st.columns(2)
with c3:
    st.dataframe(loc_data, use_container_width=True, height=200)
with c4:
    # hasClicked = card(
    #     title=str(pay_data) + " Kč/měsíc",
    #     text="Median salary",
    #     image="https://images.unsplash.com/photo-1561414927-6d86591d0c4f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80",
    # )
    st.metric(label="Median Pay", value=str(pay_data) + " Kč/měsíc")
    st.metric(label="Number of jobs", value=str(df.shape[0]))

chart = st.altair_chart(c, theme="streamlit", use_container_width=True)
