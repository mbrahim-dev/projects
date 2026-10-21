from html import escape
import re

import streamlit as st
from streamlit_echarts import st_echarts


HTML_PATH = "/mount/src/projects/data/new_projects/streamlit/dev/assets/html/components.html"


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
