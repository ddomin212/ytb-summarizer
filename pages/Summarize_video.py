import streamlit as st

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized
from utils.render import bard_request, language_select

st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("✉️ Summarize video")
st.caption(
    "Maximum duration is 2 hours, otherwise you will get an error. If your video has no subtitles, you'll have to wait longer ⏳ since we have to transcribe it first."
)
if bard_request():
    link_4 = st.text_input("YouTube URL 🔗")
    select_in4, select_out4, confirm = language_select(languages_with_flags,flag="summarize")

    if link_4 and select_in4 and select_out4 and confirm:
        first_time = is_kaggle_initialized()
        try:
            response = get_kaggle(
                select_in4,
                select_out4,
                "video",
                link_4,
                "summarize",
                "",
                first_time,
            )
        except FileNotFoundError as e:
            st.error("Our servers are on 🔥, please try again later")
            raise e
        st.write(response)
