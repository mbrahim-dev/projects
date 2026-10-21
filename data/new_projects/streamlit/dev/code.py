from html import escape
from pathlib import Path
import re

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from page_home import render_home_page
from page_overview import render_overview_page
from page_time_analysis import render_time_analysis_page
from page_product_analysis import render_product_analysis_page
from page_geographical_analysis import render_geographical_analysis_page

# configure the application

st.set_page_config(
    page_title="My Streamlit App",
    layout="wide",
)

# load CSS

with open(
    "/mount/src/projects/data/new_projects/streamlit/dev/assets/css/style.css",
    encoding="utf-8",
) as file:
    css = file.read()

st.markdown(
    f"<style>\n{css}\n</style>",
    unsafe_allow_html=True,
)

# load dataset

df1 = pd.read_csv(
    "/mount/src/projects/data/new_projects/streamlit/dataset/sales_performance.csv"
)

# shared HTML components

def render_html_template(component_name: str, **values) -> None:
    with open(
        "/mount/src/projects/data/new_projects/streamlit/dev/assets/html/components.html",
        encoding="utf-8",
    ) as file:
        source = file.read()

    pattern = (
        rf"<!-- component: {re.escape(component_name)} -->"
        rf"\s*(.*?)(?=\n<!-- component: |\Z)"
    )

    match = re.search(pattern, source, flags=re.DOTALL)

    if match is None:
        raise ValueError(
            f"HTML component not found: {component_name}"
        )

    template = match.group(1).strip()

    safe_values = {
        key: escape(str(value))
        for key, value in values.items()
    }

    st.markdown(
        template.format(**safe_values),
        unsafe_allow_html=True,
    )


def render_metric_value(value) -> None:
    render_html_template(
        "metric_value",
        value=value,
    )


def render_metric_delta(
    *,
    color: str,
    delta: str,
    label: str,
) -> None:
    render_html_template(
        "metric_delta",
        color=color,
        delta=delta,
        label=label,
    )


def render_metric_delta_empty() -> None:
    render_html_template("metric_delta_empty")


def render_progress_bar(
    *,
    progress: str,
    color: str,
) -> None:
    render_html_template(
        "progress_bar",
        progress=progress,
        color=color,
    )

# sidebar navigation

with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=["Home", "Data Visualization"],
        icons=["house", "bar-chart-line"],
        menu_icon=None,
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent",
            },
            "icon": {
                "color": "#64748B",
                "font-size": "18px",
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "10px 12px",
                "border-radius": "8px",
                "background-color": "transparent",
                "color": "#64748B",
            },
            "nav-link-selected": {
                "background-color": "#E8EDF3",
                "color": "#1E293B",
                "font-size": "15px",
                "font-weight": "600",
            },
        },
    )

# display selected page

if page == "Home":
    render_home_page()

elif page == "Data Visualization":
    sp1, sp2, pagination_col, sp4, sp5 = st.columns(5)

    with pagination_col:
        page_analysis = st.pagination(4)

    st.subheader("")

    if page_analysis == 1:
        render_overview_page(df1)

    elif page_analysis == 2:
        render_time_analysis_page(df1)

    elif page_analysis == 3:
        render_product_analysis_page(df1)

    elif page_analysis == 4:
        render_geographical_analysis_page(df1)
