import streamlit as st

from utils.countries import languages_with_flags
from utils.render import bard_request, language_select, exception_handler
from utils.classes.interface import StreamlitPage
from utils.classes.kaggle import KaggleAPI

class SummarizeCommentsPage(StreamlitPage):
    def setup_page(self):
        st.header("✉️ Summarize comments from video")
        st.caption("Might not be all the comments, but most of them will be analyzed")
        self.kaggle = KaggleAPI(what="comments", type="summarize")

    def input_handling(self):
        if bard_request():
            link_3 = st.text_input("YouTube URL 🔗")
            select_in3, select_out3, confirm = language_select(languages_with_flags,flag="summarize")
            if link_3 and select_in3 and select_out3 and confirm:
                self.get_summary(link_3, select_in3, select_out3)

    @exception_handler
    def get_summary(self, link_3, select_in3, select_out3):
        response = self.kaggle.video_query(
            select_in3,
            select_out3,
            link_3,
        )
        st.write(response)

if __name__ == "__main__":
    SummarizeCommentsPage().render()
