# application entry point and shared functions

from html import escape
from pathlib import Path
import re
import sys

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_option_menu import option_menu

# resource and dataset paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
DATASET_PATH = PROJECT_ROOT / "dataset" / "sales_performance.csv"

# loading external resources

def load_text_asset(relative_path: str) -> str:

    # load a text asset from the assets directory

    return (ASSETS_DIR / relative_path).read_text(encoding="utf-8")

def load_styles_html() -> str:

    # wrap the external stylesheet in a style element for streamlit

    stylesheet = load_text_asset("css/style.css")
    return f"<style>\n{stylesheet}\n</style>"

def render_html_template(component_name: str, **values) -> None:

    # render a named html component with escaped dynamic values

    source = load_text_asset("html/components.html")
    pattern = rf"<!-- component: {re.escape(component_name)} -->\s*(.*?)(?=\n<!-- component: |\Z)"
    match = re.search(pattern, source, flags=re.DOTALL)
    if match is None:
        raise ValueError(f"html component not found: {component_name}")
    template = match.group(1).strip()
    safe_values = {key: escape(str(value)) for key, value in values.items()}
    st.markdown(template.format(**safe_values), unsafe_allow_html=True)

# affichage des indicateurs et des graphiques

def render_metric_value(value) -> None:
    render_html_template("metric_value", value=value)

def render_metric_delta(*, color: str, delta: str, label: str) -> None:
    render_html_template("metric_delta", color=color, delta=delta, label=label)

def render_metric_delta_empty() -> None:
    render_html_template("metric_delta_empty")

def render_progress_bar(*, progress: str, color: str) -> None:
    render_html_template("progress_bar", progress=progress, color=color)

def render_echarts_chart(options: dict, **kwargs) -> None:

    # render a chart with streamlit's echarts integration

    st.echarts_chart(options, **kwargs)

def render_streamlit_echarts(options: dict, **kwargs) -> None:

    # render an echarts chart through streamlit-echarts

    st_echarts(options=options, **kwargs)

def render_sidebar() -> str:

    # display the main navigation menu and return the selected page

    main = "Home"
    p1 = "Data Visualization"
    with st.sidebar:
        page = option_menu(
            menu_title=None,
            options=[main, p1],
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
    return page

# lancement de l'application streamlit

def main() -> None:

    # load the dataset and route the user to the selected page

    from dev.page_home import render_home_page
    from dev.page_overview import render_overview_page
    from dev.page_time_analysis import render_time_analysis_page
    from dev.page_product_analysis import render_product_analysis_page
    from dev.page_geographical_analysis import render_geographical_analysis_page

    df1 = pd.read_csv(DATASET_PATH)

    st.set_page_config("", "", layout="wide")

    st.error("TEST: UPDATED CODE.PY")

    st.markdown(load_styles_html(), unsafe_allow_html=True)
    
    page = render_sidebar()

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

if __name__ == "__main__":
    main()
