import os

import streamlit as st

from views import ask_comments, ask_video, sum_comments, sum_video

if os.getenv("MODE") != "production":
    from dotenv import load_dotenv

    load_dotenv()
st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("Breeze through long videos and comments with this tool!")

st.markdown(
    """Using the power of GPT-3.5-Turbo and vector databases you can cut that
            5 hour podcast to a few minutes, or your comments to just a few sentences, keeping the 80/20 workflow."""
)

c1, c2 = st.columns(2)
with c1:
    how = st.selectbox(
        "Select what you want to do with the video", ["Ask", "Summarize"]
    )
with c2:
    what = st.selectbox(
        "Select what you want to summarize", ["Video", "Comments"]
    )

st.divider()
if how == "Ask":
    if what == "Video":
        ask_video()
    else:
        ask_comments()
else:
    if what == "Video":
        sum_video()
    else:
        sum_comments()
