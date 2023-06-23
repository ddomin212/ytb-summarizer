import textwrap

import streamlit as st
from streamlit_player import st_player

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized


def ask_video():
    st.header("💬 Chat with your video!")
    st.caption(
        "duration not limited, but you'll have to ask a certain question. If your video has no subtitles, you'll have to wait longer ⏳ since we have to transcribe it first."
    )
    link_1 = st.text_input("YouTube URL 🔗")
    query = st.text_input(
        "❓ Ask a question about the video (sane language as input)"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        select_in1 = st.selectbox(
            "Select input language ⬇️",
            languages_with_flags.keys(),
            key="select_in1",
        )
    with col2:
        select_out1 = st.selectbox(
            "Select output language ⬆️",
            languages_with_flags.keys(),
            key="select_out1",
        )
    with col3:
        select_q1 = st.selectbox(
            "Select query language ❔",
            languages_with_flags.keys(),
            key="select_q1",
        )
    confirm = st.button("Confirm ✔️", key="confirm1")

    if (
        link_1
        and query
        and select_in1
        and select_out1
        and select_q1
        and confirm
    ):
        st_player(link_1, height=600)
        first_time = is_kaggle_initialized()
        with st.spinner("Searching for answer..."):
            try:
                response = get_kaggle(
                    select_in1,
                    select_out1,
                    "video",
                    link_1,
                    "chat",
                    query,
                    first_time,
                    qlang=select_q1,
                )
            except FileNotFoundError:
                st.error(
                    "Sorry, the video is too long 🎬 for our servers to handle"
                )
                st.stop()
        st.snow()
        st.write(textwrap.fill(response, width=50))
