import textwrap

import streamlit as st
from streamlit_player import st_player

from utils.countries import languages_with_flags
from utils.kaggle import get_kaggle, is_kaggle_initialized
from utils.render import bard_request, language_select

st.set_page_config(page_title="AskTube", page_icon="📷", layout="wide")
st.header("💬 Chat with your video!")
st.caption(
    "duration not limited, but you'll have to ask a certain question. If your video has no subtitles, you'll have to wait longer ⏳ since we have to transcribe it first."
)
if bard_request():
    link_1 = st.text_input("YouTube URL 🔗")
    query = st.text_input(
        "❓ Ask a question about the video (sane language as input)"
    )
    select_in1, select_out1, select_q1, confirm = language_select(languages_with_flags,)
    if link_1 and query and select_in1 and select_out1 and select_q1 and confirm:
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
            except FileNotFoundError as e:
                st.error(
                    "Sorry, the video is too long 🎬 for our servers to handle"
                )
                raise e
        st.snow()
        st.write(textwrap.fill(response, width=50))
