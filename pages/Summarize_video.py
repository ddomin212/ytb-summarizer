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
link_4 = st.text_input("YouTube URL 🔗")

if link_4:
    first_time = is_kaggle_initialized("video")
    try:
        response = get_kaggle("video", link_4, "summarize", "", first_time)
    except FileNotFoundError:
        st.error("Our servers are on 🔥, please try again later")
        st.stop()
    st.write(response)
