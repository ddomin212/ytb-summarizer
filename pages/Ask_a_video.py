import textwrap
import streamlit as st
from streamlit_player import st_player
from utils.kaggle_helpers import get_kaggle, is_kaggle_initialized

st.set_page_config(page_title="AskTube", page_icon="📷", layout="wide")
st.header("💬 Chat with your video!")
st.caption("duration not limited, but you'll have to ask a certain question")
link_1 = st.text_input("YouTube URL 🔗")


if link_1:
    st_player(link_1, height=600)
    query = st.text_input("❓ Ask a question about the video")
    if query:
        first_time = is_kaggle_initialized("video")
        with st.spinner("Searching for answer..."):
            try:
                response = get_kaggle(
                    "video", link_1, "chat", query, first_time
                )
            except FileNotFoundError:
                st.error(
                    "Sorry, the video is too long 🎬 for our servers to handle"
                )
                st.stop()
        st.snow()
        st.write(textwrap.fill(response, width=50))
