import streamlit as st

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized
from utils.render import bard_request, language_select

st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("✉️ Summarize comments from video")
st.caption("Might not be all the comments, but most of them will be analyzed")

if bard_request():
    link_3 = st.text_input("YouTube URL 🔗")
    select_in3, select_out3, confirm = language_select(languages_with_flags,flag="summarize")

    if link_3 and select_in3 and select_out3 and confirm:
        first_time = is_kaggle_initialized()
        try:
            response = get_kaggle(
                select_in3,
                select_out3,
                "comments",
                link_3,
                "summarize",
                "",
                first_time,
            )
        except FileNotFoundError:
            st.error("Our servers are on 🔥, please try again later")
            st.stop()
        st.write(response)
