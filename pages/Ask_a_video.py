import textwrap

import streamlit as st
from streamlit_player import st_player

from utils.countries import languages_with_flags
from utils.render import bard_request, language_select, exception_handler
from utils.classes.interface import StreamlitPage
from utils.classes.kaggle import KaggleAPI

class AskAVideoPage(StreamlitPage):
    def setup_page(self):
        st.header("💬 Chat with your video!")
        st.caption(
            "duration not limited, but you'll have to ask a certain question. If your video has no subtitles, you'll have to wait longer ⏳ since we have to transcribe it first."
        )
        self.kaggle = KaggleAPI(what="video", type="chat")
    
    def input_handling(self):
        if bard_request():
            link_1 = st.text_input("YouTube URL 🔗")
            query = st.text_input(
                "❓ Ask a question about the video (sane language as input)"
            )
            select_in1, select_out1, select_q1, confirm = language_select(languages_with_flags,)
            if link_1 and query and select_in1 and select_out1 and select_q1 and confirm:
                self.get_query(link_1, query, select_in1, select_out1, select_q1)
    
    @exception_handler
    def get_query(self, link_1, query, select_in1, select_out1, select_q1):
        st_player(link_1, height=600)
        with st.spinner("Searching for answer..."):
            response = self.kaggle.video_query(
                select_in1,
                select_out1,
                link_1,
                query,
                qlang=select_q1
            )
        st.snow()
        st.write(textwrap.fill(response, width=50))

if __name__ == "__main__":
    AskAVideoPage().render()
