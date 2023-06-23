import streamlit as st

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized


def sum_comments():
    st.header("✉️ Summarize comments from video")
    st.caption(
        "Might not be all the comments, but most of them will be analyzed"
    )
    link_3 = st.text_input("YouTube URL 🔗")
    select_in3 = st.selectbox(
        "Select input language 🌐",
        languages_with_flags.keys(),
        key="select_in3",
    )
    select_out3 = st.selectbox(
        "Select output language 🌐",
        languages_with_flags.keys(),
        key="select_out3",
    )
    confirm = st.button("Confirm ✔️", key="confirm3")

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
