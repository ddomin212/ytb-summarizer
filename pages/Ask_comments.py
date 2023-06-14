import textwrap
import streamlit as st
from streamlit_player import st_player
from utils.kaggle_helpers import get_kaggle, is_kaggle_initialized

st.set_page_config(page_title="AskTube", page_icon="📷", layout="wide")
st.header("💬 Chat with your comments!")
st.caption("Might not be all the comments, but most of them will be analyzed")
link_2 = st.text_input("YouTube URL 🔗")


if link_2:
    st_player(link_2, height=600)
    query = st.text_input("❓ What do you want to know about the comments?")
    if query:
        first_time = is_kaggle_initialized("comments")
        with st.spinner("Searching for answer..."):
            try:
                response = get_kaggle(
                    "comments", link_2, "chat", query, first_time
                )
            except FileNotFoundError:
                st.error("Our servers are on 🔥, please try again later")
                st.stop()
        st.snow()
        st.write(textwrap.fill(response, width=50))
