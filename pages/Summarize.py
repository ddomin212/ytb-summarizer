import os
import streamlit as st
from utils.kaggle_helpers import get_kaggle, is_kaggle_initialized


st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("✉️ Summarize video")
st.caption("maximum duration is 2 hours, otherwise you will get an error")
link = st.text_input("Youtube Link")

if link:
    first_time = is_kaggle_initialized()
    try:
        response = get_kaggle(link, "summarize", "", first_time)
    except FileNotFoundError:
        st.error("Our servers are on 🔥, please try again later")
        st.stop()
    st.write(response)
