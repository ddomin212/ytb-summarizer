import textwrap

import streamlit as st
from streamlit_player import st_player

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized

st.set_page_config(page_title="AskTube", page_icon="📷", layout="wide")
st.header("💬 Chat with your comments!")
st.caption("Might not be all the comments, but most of them will be analyzed")
link_2 = st.text_input("YouTube URL 🔗")
query = st.text_input(
    "❓ What do you want to know about the comments? (Same language as input)"
)
col1, col2, col3 = st.columns(3)
with col1:
    select_in2 = st.selectbox(
        "Select input language ⬇️",
        languages_with_flags.keys(),
        key="select_in2",
    )
with col2:
    select_out2 = st.selectbox(
        "Select output language ⬆️",
        languages_with_flags.keys(),
        key="select_out2",
    )
with col3:
    select_q2 = st.selectbox(
        "Select query language ❔",
        languages_with_flags.keys(),
        key="select_q2",
    )
confirm = st.button("Confirm ✔️", key="confirm2")

if link_2 and query and select_in2 and select_out2 and select_q2 and confirm:
    st_player(link_2, height=600)
    first_time = is_kaggle_initialized()
    with st.spinner("Searching for answer..."):
        try:
            response = get_kaggle(
                select_in2,
                select_out2,
                "comments",
                link_2,
                "chat",
                query,
                first_time,
                qlang=select_q2,
            )
        except FileNotFoundError:
            st.error("Our servers are on 🔥, please try again later")
            st.stop()
    st.snow()
    st.write(textwrap.fill(response, width=50))
