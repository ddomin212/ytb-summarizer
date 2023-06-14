import streamlit as st
from utils.kaggle_helpers import get_kaggle, is_kaggle_initialized


st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("✉️ Summarize comments from video")
st.caption("Might not be all the comments, but most of them will be analyzed")
link_3 = st.text_input("YouTube URL 🔗")

if link_3:
    first_time = is_kaggle_initialized("comments")
    try:
        response = get_kaggle("comments", link_3, "summarize", "", first_time)
    except FileNotFoundError:
        st.error("Our servers are on 🔥, please try again later")
        st.stop()
    st.write(response)
