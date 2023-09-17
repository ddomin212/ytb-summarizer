import altair as alt
import streamlit as st


def filters(key_name):
    """
    Initializes filters for the streamlit app dashboard.

    Args:
        key_name (str): The name of the filter. Either "data", "devops" or "web".

    Returns:
        tuple: A tuple of two strings, the first one is the location fiter value,
                the second one is the seniority filter value.
    """
    c1, c2 = st.columns(2)
    with c1:
        misto = st.selectbox(
            "Místo",
            ["Celá ČR", "Praha", "Brno"],
            key=f"loc_{key_name}",
        )
    with c2:
        seniorita = st.selectbox(
            "Senorita",
            ["Všechny", "Junior", "Senior"],
            key=f"pozice_{key_name}",
        )
    return misto, seniorita


def plot_chart(tech_data):
    """create an altair chart showing the number of jobs for each technology

    Args:
        tech_data: dataframe including the number of jobs for each technology

    Returns:
        altar chart
    """
    alt.data_transformers.enable("default", max_rows=None)
    alt.renderers.set_embed_options(dpi=300)
    c = (
        alt.Chart(tech_data[tech_data.Count > 2])
        .mark_bar()
        .encode(
            x="Count:Q",
            y=alt.Y("Tech:N", sort="-x"),  # Sort the bars in descending order
            tooltip=["Tech", "Count", "Branch"],
            color="Branch:N",
        )
    )
    return c


def detail(loc_data, pay_data):
    """plot the detailed info on the pay and number of jobs

    Args:
        loc_data: number of jobs in all locations
        pay_data: median pay in a given location
    """
    c3, c4 = st.columns(2)
    with c3:
        st.dataframe(loc_data, use_container_width=True, height=200)
    with c4:
        st.metric(label="Median Pay", value=str(pay_data) + " Kč/měsíc")
        st.metric(
            label="Number of jobs", value=str(sum(loc_data.values.tolist()))
        )
