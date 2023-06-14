import streamlit as st
from utils.ideation import video_ideation


st.set_page_config(
    page_title="SummarizeTube",
    page_icon="🤖",
    layout="wide",
)
st.header("📄 Draft video script & thumbnail & title")
st.caption("maximum duration is 2 hours, otherwise you will get an error")
abstract = st.text_area(label="🖊️ Video abstract", max_chars=2000)

if abstract:
    response = video_ideation(abstract)
    st.subheader("🔥 Video title")
    st.write(response["title"])
    st.subheader("🖼️ Thumbnail")
    st.write(response["thumbnail"])
    st.subheader("📝 Video script")
    st.write(response["script"])
