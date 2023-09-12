import streamlit as st
from utils.general import is_prod

is_prod()

st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("Watching through a 5 hour podcast? Well I am not doing that...")

st.write(
    """I will summarize it for you! Using the power of GPT-3.5-Turbo and vector databases you can cut that
            5 hour podcast to a few minutes, while keeping all the essential information!"""
)
