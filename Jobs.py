import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

from data_utils.parse import get_locations, get_pay, select_job_position
from data_utils.scrape import check_date, load_data
from data_utils.st_utils import detail, filters, plot_chart

load_dotenv()
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
loc_data = get_locations(df, misto, seniorita)
pay_data = get_pay(df, misto, seniorita)


st.divider()
detail(loc_data, pay_data)

c = plot_chart(tech_data)
st.altair_chart(c, theme="streamlit", use_container_width=True)
