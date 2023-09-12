import os

import altair as alt
import streamlit as st
from streamlit_option_menu import option_menu

from data_utils.date_check import check_date
from data_utils.parse_jobs import get_locations, get_pay
from data_utils.st_utils import filters, load_data, select_job_position, plot_chart, detail
from utils.general import is_prod

is_prod()
check_date()

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
df, devops, data, web = load_data()

tech_data = select_job_position(selected, df, misto, devops, data, web)
loc_data = get_locations(df, seniorita)
pay_data = get_pay(df, seniorita)


st.divider()
detail(loc_data, pay_data)

c = plot_chart(tech_data)
st.altair_chart(c, theme="streamlit", use_container_width=True)
