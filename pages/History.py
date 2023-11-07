import streamlit as st

from utils.classes.interface import StreamlitPage
from utils.firebase import db

class History(StreamlitPage):
    def setup_page(self):
        st.header("💬 Prompt history")
        items = db.child(st.session_state.user['localId']).child("history").get().val()
        for i in items:
            with st.container():
                items[i]["link"] = f"https://www.youtube.com/watch?v={i}"
                st.table(items[i])
    def input_handling(self):
        pass

if __name__ == "__main__":
    History().render()
