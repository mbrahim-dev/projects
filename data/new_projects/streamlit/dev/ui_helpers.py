from html import escape
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def load_text_asset(relative_path: str) -> str:
    """Load a UTF-8 text asset located under dev/assets."""
    return (ASSETS_DIR / relative_path).read_text(encoding="utf-8")


def load_styles_html() -> str:
    """Combine the external CSS file with its HTML wrapper template."""
    wrapper = load_text_asset("html/styles.html")
    stylesheet = load_text_asset("css/style.css")
    return wrapper.replace("{css}", stylesheet)


def render_html_template(template_name: str, **values) -> None:
    """Render an external HTML template with escaped text values."""
    template = load_text_asset(f"html/{template_name}")
    safe_values = {key: escape(str(value)) for key, value in values.items()}
    st.markdown(template.format(**safe_values), unsafe_allow_html=True)
