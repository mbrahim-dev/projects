from html import escape
import re

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from dev.page_home import render_home_page
from dev.page_overview import render_overview_page
from dev.page_time_analysis import render_time_analysis_page
from dev.page_product_analysis import render_product_analysis_page
from dev.page_geographical_analysis import render_geographical_analysis_page


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
    f"<style>{css}</style>",
    unsafe_allow_html=True,
)


# load dataset

df = pd.read_csv(
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

    match = re.search(
        pattern,
        source,
        flags=re.DOTALL,
    )

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
        options=[
            "Home",
            "Data Visualization",
        ],
        icons=[
            "house",
            "bar-chart-line",
        ],
        default_index=0,
        orientation="vertical",
    )


# display selected page

if page == "Home":
    render_home_page()

else:
    page_analysis = st.pagination(
        "Select a page",
        options=[
            "Overview",
            "Time Analysis",
            "Product Analysis",
            "Geographical Analysis",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )

    if page_analysis == "Overview":
        render_overview_page(df)

    elif page_analysis == "Time Analysis":
        render_time_analysis_page(df)

    elif page_analysis == "Product Analysis":
        render_product_analysis_page(df)

    elif page_analysis == "Geographical Analysis":
        render_geographical_analysis_page(df)
