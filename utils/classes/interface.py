from abc import ABCMeta, abstractmethod
from utils.firebase import auth
import streamlit as st

class StreamlitPage(metaclass=ABCMeta):
    def authenticate(self, tag):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.button("Log in")
        if confirm and email and password:
            if tag == "Sign up":
                user = auth.create_user_with_email_and_password(email, password)
            else:
                user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.experimental_rerun()

    def render(self):
        with st.expander("Authentication", expanded=not hasattr(st.session_state, "user")):
            option = st.selectbox(
                "Select an option",
                ["Sign up", "Log in"],
            )
            if option:
                self.authenticate(option)
        if hasattr(st.session_state, "user"):
            with st.expander("Get response", expanded=hasattr(st.session_state, "user")):
                self.setup_page()
                self.input_handling()

    @abstractmethod
    def setup_page(self):
        pass

    @abstractmethod
    def input_handling(self):
        pass