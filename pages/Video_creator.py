import streamlit as st
from utils.ideation import video_ideation
from utils.classes.interface import StreamlitPage
from utils.render import exception_handler

class VideoCreatorPage(StreamlitPage):
    def setup_page(self):
        st.set_page_config(
            page_title="SummarizeTube",
            page_icon="🤖",
            layout="wide",
        )
        st.header("📄 Draft video script & thumbnail & title")
        
    
    def input_handling(self):
        abstract = st.text_area(label="🖊️ Video abstract", max_chars=2000)
        if abstract:
            self.get_ideas(abstract)

    @exception_handler        
    def get_ideas(self, abstract):
        response = video_ideation(abstract)
        st.subheader("🔥 Video title")
        st.write(response["title"])
        st.subheader("🖼️ Thumbnail")
        st.write(response["thumbnail"])
        st.subheader("📝 Video script")
        st.write(response["script"])


if __name__ == "__main__":
    VideoCreatorPage().render()