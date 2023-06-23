import streamlit as st

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized


def sum_video():
    st.header("✉️ Summarize video")
    st.caption(
        "Maximum duration is 2 hours, otherwise you will get an error. If your video has no subtitles, you'll have to wait longer ⏳ since we have to transcribe it first."
    )
    link_4 = st.text_input("YouTube URL 🔗")
    select_in4 = st.selectbox(
        "Select input language 🌐",
        languages_with_flags.keys(),
        key="select_in4",
    )
    select_out4 = st.selectbox(
        "Select output language 🌐",
        languages_with_flags.keys(),
        key="select_out4",
    )
    confirm = st.button("Confirm ✔️", key="confirm4")

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
        except FileNotFoundError:
            st.error("Our servers are on 🔥, please try again later")
            st.stop()
        st.write(response)
