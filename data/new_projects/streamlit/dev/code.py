from html import escape
import importlib.util
import re
import sys

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_option_menu import option_menu


# absolute paths

HOME_PAGE_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/page_home.py"
OVERVIEW_PAGE_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/page_overview.py"
TIME_PAGE_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/page_time_analysis.py"
PRODUCT_PAGE_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/page_product_analysis.py"
GEOGRAPHICAL_PAGE_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/page_geographical_analysis.py"

CSS_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/assets/css/style.css"
HTML_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/assets/html/components.html"
DATASET_PATH = "/mount/src/projects/data/new_projects/streamlit/dataset/sales_performance.csv"


# configure streamlit

st.set_page_config(page_title="My Streamlit App", layout="wide")


# load css

with open(CSS_PATH, encoding="utf-8") as file:
    css = file.read()

st.markdown(f"<style>\n{css}\n</style>", unsafe_allow_html=True)


# load dataset

df1 = pd.read_csv(DATASET_PATH)


# load a python page from its absolute path

def load_page_function(file_path: str, function_name: str):
    module_name = "streamlit_page_" + function_name

    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load page file: {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise

    return getattr(module, function_name)


# shared html components

def render_html_template(component_name: str, **values) -> None:
    with open(HTML_PATH, encoding="utf-8") as file:
        source = file.read()

    pattern = (
        rf"<!-- component: {re.escape(component_name)} -->"
        rf"\s*(.*?)(?=\n<!-- component: |\Z)"
    )

    match = re.search(pattern, source, flags=re.DOTALL)

    if match is None:
        raise ValueError(f"HTML component not found: {component_name}")

    template = match.group(1).strip()
    safe_values = {key: escape(str(value)) for key, value in values.items()}

    st.markdown(
        template.format(**safe_values),
        unsafe_allow_html=True,
    )


def render_metric_value(value) -> None:
    render_html_template("metric_value", value=value)


def render_metric_delta(*, color: str, delta: str, label: str) -> None:
    render_html_template(
        "metric_delta",
        color=color,
        delta=delta,
        label=label,
    )


def render_metric_delta_empty() -> None:
    render_html_template("metric_delta_empty")


def render_progress_bar(*, progress: str, color: str) -> None:
    render_html_template(
        "progress_bar",
        progress=progress,
        color=color,
    )


def render_echarts_chart(options: dict, **kwargs) -> None:
    st.echarts_chart(options, **kwargs)


def render_streamlit_echarts(options: dict, **kwargs) -> None:
    st_echarts(options=options, **kwargs)


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


# load only the selected page

if page == "Home":
    render_home_page = load_page_function(
        HOME_PAGE_PATH,
        "render_home_page",
    )
    render_home_page()

elif page == "Data Visualization":
    sp1, sp2, pagination_col, sp4, sp5 = st.columns(5)

    with pagination_col:
        page_analysis = st.pagination(4)

    st.subheader("")

    if page_analysis == 1:
        render_overview_page = load_page_function(
            OVERVIEW_PAGE_PATH,
            "render_overview_page",
        )
        render_overview_page(df1)

    elif page_analysis == 2:
        render_time_analysis_page = load_page_function(
            TIME_PAGE_PATH,
            "render_time_analysis_page",
        )
        render_time_analysis_page(df1)

    elif page_analysis == 3:
        render_product_analysis_page = load_page_function(
            PRODUCT_PAGE_PATH,
            "render_product_analysis_page",
        )
        render_product_analysis_page(df1)

    elif page_analysis == 4:
        render_geographical_analysis_page = load_page_function(
            GEOGRAPHICAL_PAGE_PATH,
            "render_geographical_analysis_page",
        )
        render_geographical_analysis_page(df1)
