# import librairies

import streamlit as st
import pandas as pd

# import datasets

df1 = pd.read_csv("data/new_projects/streamlit/datasets/sales_performance.csv")
columns_df1 = ["category","product","quantity","unit_price","discount_rate","revenue","cost","profit","country","sales_channel"]

# page config

st.set_page_config("", "", layout="wide")

# creating pages

main = "🏠 Home"
p1 = "📈 Sales Performance"

# sidebar

page = st.sidebar.radio(
    "Navigation",
    [main, p1]
)

# home page

if page == main:

    st.header("Welcome to my Streamlit App 👋")

    st.caption("")

    st.divider()

    st.caption("")
    
    st.markdown("""On this home page, you will find answers to some of the key questions you may have about this application and the technology behind it.""")

    st.divider()

    st.subheader("1 - What is a Streamlit App ❓")

    st.caption("")

    st.markdown("""An interactive web application.""")

    st.caption("")

    st.subheader("2 - What will you find in this application ❓")

    st.caption("")

    st.markdown("""Different **projects that can be built with Streamlit**.""")

    st.caption("")

    st.subheader("3 - Why use Streamlit ❓")

    st.caption("")

    st.markdown("""A simple way to turn **data into interactive visualizations**.""")

    st.caption("")

    st.subheader("4 - How is a Streamlit App built ❓")

    st.caption("")

    st.markdown("""Mainly with **Python code**, but you can also use **CSS** to customize its design.""")
    

# page 1

elif page == p1:

    # pagination

    p1_col, p2_col, p3_col, p4_col, p5_col = st.columns(5)

    with p3_col:
        page_analysis = st.pagination(4)

    st.subheader("")
    
    # overview

    if page_analysis == 1:

        st.title("📊 Sales Performance Overview")

        st.subheader("")

        s1, s2, s3, s4, s5 = st.columns(5)

        with s1:
            category = st.selectbox(
                "🏷️ Product Category",
                df1["category"].unique()
            )

        with s3:
            country = st.selectbox(
                "🌍 Country",
                df1["country"].unique()
            )

        with s5:
            sales_channel = st.selectbox(
                "🛒 Sales Channel",
                df1["sales_channel"].unique()
            )

        filtered_df1 = df1[
            (df1["category"] == category) &
            (df1["country"] == country) &
            (df1["sales_channel"] == sales_channel)
        ]

        st.subheader("")

        st.dataframe(filtered_df1[columns_df1])

        st.subheader("")

        m1, m2, m3, m4, m5, m6, m7, m8, m9 = st.columns(9)

        m2.metric(
            "💰 Revenue",
            f"${filtered_df1['revenue'].sum():,.0f}"
        )

        m4.metric(
            "📈 Profit",
            f"${filtered_df1['profit'].sum():,.0f}"
        )

        m6.metric(
            "📦 Orders",
            f"{filtered_df1['order_id'].nunique():,}"
        )

        m8.metric(
            "💵 Avg. Order Value",
            f"${filtered_df1['revenue'].sum() / filtered_df1['order_id'].nunique():,.0f}"
        )


    # time analysis

    elif page_analysis == 2:

        st.title("📅 Time Analysis")


    # geographic analysis

    elif page_analysis == 3:

        st.title("🌍 Geographic Analysis")


    # product analysis

    elif page_analysis == 4:

        st.title("🏷️ Product Analysis")
