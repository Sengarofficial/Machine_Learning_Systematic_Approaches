import streamlit as st

from app.utils import img_to_bytes
from app.plots import (
    lineplot_cumulative_daily_deaths,
    lineplot_daily_deaths
)


def main_title():
    # Dashboard title
    st.title('COVID-19 deaths analysis')


def add_main_title(view):
    def wrapper(*args, **kwargs):
        main_title()
        view(*args, **kwargs)
    return wrapper


def navbar():
    # Sidebar
    st.sidebar.title('Navigation Bar')

    # Views
    view = st.sidebar.radio(
        'Select one',
        ('Cumulative deaths', 'Daily deaths'),
        index=0
    )

    normalize = st.sidebar.checkbox(
        'Normalize deaths (per million people)',
        value=True
    )

    # Italian regions image
    header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=100%>".format(
        img_to_bytes("./imgs/italy_regions-wanderingitaly.com.png")
    )
    st.sidebar.markdown(
        header_html, unsafe_allow_html=True,
    )
    return view, normalize


@add_main_title
def cumulative_daily_deaths_view(data):
    st.header('Cumulative daily deaths during 2020')
    st.altair_chart(
        lineplot_cumulative_daily_deaths(data)
    )


@add_main_title
def daily_deaths_view(config, data):
    st.header('Daily deaths during 2020')

    selected_region = st.selectbox(
        'Regions',
        config.REGIONS
    )
    
    st.altair_chart(
        lineplot_daily_deaths(data, selected_region)
    )