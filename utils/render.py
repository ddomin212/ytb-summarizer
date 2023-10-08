import streamlit as st

from functools import wraps
from random import choice

import streamlit as st

ERROR_ICONS = ["⚠️", "🚫", "🛑", "🔥", "🤯", "🤬", "👺", "👹", "👿", "💀", "☠️"]


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(body=e, icon=choice(ERROR_ICONS))
            raise e

    return wrapper

def bard_request():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state._1PSID = st.text_input("Your Bard _1PSID Cookie:")
    with c2:
        st.session_state._1PSIDTS = st.text_input("Your Bard _1PSIDTS Cookie:")
    with c3:
        st.session_state._1PSIDCC = st.text_input("Your Bard _1PSIDCC Cookie:")
    st.divider()
    if st.session_state._1PSID and st.session_state._1PSIDTS and st.session_state._1PSIDCC:
        return True
    
def language_select(languages, flag="query"):
    col1, col2, col3 = st.columns(3)
    with col1:
        select_in2 = st.selectbox(
            "Select input language ⬇️",
            languages.keys(),
            placeholder="English",
        )
    with col2:
        select_out2 = st.selectbox(
            "Select output language ⬆️",
            languages.keys(),
            placeholder="English",
        )
    with col3:
        if flag == "query":
            select_q2 = st.selectbox(
                "Select query language ❔",
                languages.keys(),
                placeholder="English",
            )
    confirm = st.button("Confirm ✔️")
    if flag == "query":
        return select_in2, select_out2, select_q2, confirm
    else:
        return select_in2, select_out2, confirm