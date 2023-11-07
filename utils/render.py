import streamlit as st

from functools import wraps
from random import choice

import streamlit as st
from utils.firebase import db

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
    cookie_dict = db.child(st.session_state.user['localId']).child("bard_cookies").get().val()
    with c1:
        st.session_state._1PSID = st.text_input("_1PSID:", value=cookie_dict["_1PSID"] if cookie_dict else "")
    with c2:
        st.session_state._1PSIDTS = st.text_input("_1PSIDTS (changes frequently):", value=cookie_dict["_1PSIDTS"] if cookie_dict else "")
    with c3:
        st.session_state._1PSIDCC = st.text_input("_1PSIDCC: (changes frequently)", value=cookie_dict["_1PSIDCC"] if cookie_dict else "")
    st.divider()
    if st.session_state._1PSID and st.session_state._1PSIDTS and st.session_state._1PSIDCC:
        db.child(st.session_state.user['localId']).child("bard_cookies").set({
            "_1PSID": st.session_state._1PSID,
            "_1PSIDTS": st.session_state._1PSIDTS,
            "_1PSIDCC": st.session_state._1PSIDCC,
        })
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