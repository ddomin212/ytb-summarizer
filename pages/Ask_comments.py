import textwrap

import streamlit as st
from streamlit_player import st_player

from utils.countries import languages_with_flags
from utils.render import bard_request, language_select, exception_handler
from utils.classes.interface import StreamlitPage
from utils.classes.kaggle import KaggleAPI

class AskCommentsPage(StreamlitPage):
    def setup_page(self):
        st.header("💬 Chat with your comments!")
        st.caption("Might not be all the comments, but most of them will be analyzed")
        self.kaggle = KaggleAPI(what="comments", type="chat")
    
    def input_handling(self):
        if bard_request():
            link_2 = st.text_input("YouTube URL 🔗")
            query = st.text_input(
                "❓ What do you want to know about the comments? (Same language as input)"
            )
            select_in2, select_out2, select_q2, confirm = language_select(languages_with_flags,)
            if link_2 and query and select_in2 and select_out2 and select_q2 and confirm:
                self.get_query(link_2, query, select_in2, select_out2, select_q2)

    @exception_handler
    def get_query(self, link_2, query, select_in2, select_out2, select_q2):
        st_player(link_2, height=600)
        with st.spinner("Searching for answer..."):
            response = self.kaggle.video_query(
                select_in2,
                select_out2,
                link_2,
                query,
                qlang=select_q2,
            )
        st.snow()
        st.write(textwrap.fill(response, width=50))

if __name__ == "__main__":
    AskCommentsPage().render()