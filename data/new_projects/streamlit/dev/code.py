# import librairies

import streamlit as st


# creating pages

main = "🏠 Home"
p1 = "📊 Page 1"


# sidebar

page = st.sidebar.radio(
    "Navigation",
    [main, p1]
)


# using pages


# home page

if page == main:

    st.set_page_config("Welcome to my Streamlit App", "👋", layout="wide")

    st.caption("")
    
    st.markdown(""" 💻 This app is built using **python and cascading style sheets**. """)

    st.caption("")
    
    st.markdown(""" 📊 The purpose of this page is to showcase my skills in **data analysis**, **visualization** and **business intelligence**. """)

    st.caption("")
    
    st.markdown(""" 🔎 Explore the **sidebar** to discover different dashboards, datasets and business contexts through various analyses. """)


# page 1
