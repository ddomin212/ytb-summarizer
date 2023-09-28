import textwrap

import streamlit as st
from streamlit_player import st_player

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized
from utils.render import bard_request, language_select

st.set_page_config(page_title="AskTube", page_icon="📷", layout="wide")
st.header("💬 Chat with your comments!")
st.caption("Might not be all the comments, but most of them will be analyzed")

if bard_request():
    link_2 = st.text_input("YouTube URL 🔗")
    query = st.text_input(
        "❓ What do you want to know about the comments? (Same language as input)"
    )
    select_in2, select_out2, select_q2, confirm = language_select(languages_with_flags,)
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
