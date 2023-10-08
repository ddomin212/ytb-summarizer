import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

from data_utils.scrape import scrape_new_data
from data_utils.render import cards, filters, chart
from data_utils.parser import Parser

load_dotenv()
scrape_new_data()

st.header("Select your desired field of work:")
selected = option_menu(
    None,
    ["Data", "Web", "DevOps", "Cloud"],
    icons=["clipboard-data-fill", "browser-chrome", "infinity", "cloud"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

misto, seniorita = filters(selected)
parsed = Parser(misto, seniorita)

tech_data, regex = parsed.select_job_position(selected)
loc_data = parsed.get_locations(regex)
pay_data = parsed.get_pay(regex)

st.divider()

cards(loc_data, pay_data)
c = chart(tech_data)
st.altair_chart(c, theme="streamlit", use_container_width=True)
