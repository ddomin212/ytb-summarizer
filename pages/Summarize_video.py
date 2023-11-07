import streamlit as st

from utils.countries import languages_with_flags
from utils.render import bard_request, language_select, exception_handler
from utils.classes.interface import StreamlitPage
from utils.classes.kaggle import KaggleAPI

class SummarizeVideoPage(StreamlitPage):
    def setup_page(self):
        st.header("✉️ Summarize video")
        st.caption(
            "Maximum duration is 2 hours, otherwise you will get an error. If your video has no subtitles, you'll have to wait longer ⏳ since we have to transcribe it first."
        )
        self.kaggle = KaggleAPI(what="video", type="summarize")
    
    def input_handling(self):
        if bard_request():
            link_4 = st.text_input("YouTube URL 🔗")
            select_in4, select_out4, confirm = language_select(languages_with_flags,flag="summarize")

            if link_4 and select_in4 and select_out4 and confirm:
                self.get_summary(link_4, select_in4, select_out4)

    @exception_handler
    def get_summary(self, link_4, select_in4, select_out4):
        response = self.kaggle.video_query(
            select_in4,
            select_out4,
            link_4,
        )
        st.write(response)

if __name__ == "__main__":
    SummarizeVideoPage().render()