# import librairies

import streamlit as st
import pandas as pd

# import datasets

df = pd.read_csv("data/new_projects/streamlit/datasets/sales_performance.csv")

# page config

st.set_page_config("", "", layout="wide")

# creating pages

main = "🏠 Home"
p1 = "📊 Page 1"


# sidebar

page = st.sidebar.radio(
    "Navigation",
    [main, p1]
)


# home page

if page == main:

    st.title("👋 Welcome to my Streamlit App")

    st.header("")
    
    st.markdown(""" 💻 This app is built using **python and cascading style sheets**. 📊 The purpose of this page is to showcase my skills in **data analysis**, **visualization** and **business intelligence**. 
    🔎 Explore the **sidebar** to discover different dashboards, datasets and business contexts through various analyses.""")

# page 1


elif page == p1:

    st.title("📈 Sales Performance Dashboard")

    st.header("")

    df = pd.read_csv("data/new_projects/streamlit/datasets/sales_performance.csv")

    st.dataframe(df)



