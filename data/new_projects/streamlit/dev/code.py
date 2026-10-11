# import librairies

import streamlit as st
import pandas as pd

# import datasets

df1 = pd.read_csv("data/new_projects/streamlit/datasets/sales_performance.csv")

# page config

st.set_page_config("", "", layout="wide")

# creating pages

main = "🏠 Home"
p1 = "📈 Data Visualisation"

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

    st.subheader("1 - What is a Streamlit App ?")

    st.caption("")

    st.markdown("""An interactive web application.""")

    st.caption("")

    st.subheader("2 - What will you find in this application ?")

    st.caption("")

    st.markdown("""**Different projects** that can be built with Streamlit.""")

    st.caption("")

    st.subheader("3 - Why use Streamlit ?")

    st.caption("")

    st.markdown("""A simple way to **turn data into interactive visualizations**.""")

    st.caption("")

    st.subheader("4 - How is a Streamlit App built ?")

    st.caption("")

    st.markdown("""Mainly with **Python code**, but you can also use **CSS (Cascading Style Sheets)** to customize its design.""")
    

# page 1

elif page == p1:

    # pagination

    p1_col, p2_col, p3_col, p4_col, p5_col = st.columns(5)

    with p3_col:
        page_analysis = st.pagination(4)

    st.subheader("")

    # dataset overview

    if page_analysis == 1:

        st.header("Data Overview 📊")

        st.subheader("")

        st.markdown("""This page provides an overview of the dataset that will be used throughout the following pages to create different visualizations. Each subsequent page will explore these data in a different way to highlight key information.""")

        st.divider()

        st.caption("")

        # dataset

        st.subheader("Dataset")

        st.caption("")

        st.dataframe(df1,width="stretch")

        st.caption("")

        st.divider()

        st.caption("")

        # data dictionary

        st.subheader("Data Dictionary")

        st.caption("")

        data_dictionary = pd.DataFrame({
            "Column": [
                "order_id",
                "order_date",
                "category",
                "product",
                "quantity",
                "unit_price",
                "discount_rate",
                "revenue",
                "cost",
                "profit",
                "country",
                "sales_channel"
            ],
            "Format": [
                "varchar",
                "date",
                "varchar",
                "varchar",
                "integer",
                "float",
                "float",
                "float",
                "float",
                "float",
                "varchar",
                "varchar"
            ],
            "Description": [
                "Order number",
                "Date of the order",
                "Product category",
                "Product name",
                "Quantity ordered",
                "Unit selling price",
                "Discount applied to the order",
                "Total revenue generated",
                "Total cost of the order",
                "Profit generated",
                "Customer's country",
                "Sales channel used for the order"
            ]
        })

        st.dataframe(
            data_dictionary,
            width="stretch",
            hide_index=True
        )


    # time analysis

    elif page_analysis == 2:

        df1["order_date"] = pd.to_datetime(df1["order_date"])
        df1["year"] = df1["order_date"].dt.year
        df1["month"] = df1["order_date"].dt.month
        df1["month_name"] = df1["order_date"].dt.strftime("%B")
        df1["quarter"] = df1["order_date"].dt.quarter
    
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
        title_col, space_col, filters_col = st.columns([3, 3, 2])
    
        with title_col:
            st.caption("")
            st.header("Time Analysis 📅")
    
        with filters_col:
            st.markdown("**Filters**")
            year_col, month_col, quarter_col = st.columns(3)
    
            # year filter
            
            with year_col:
                with st.popover("Year"):
                    selected_years = st.multiselect("Select years", sorted(df1["year"].unique()), default=[2025])
    
            # month filter
            
            with month_col:
                with st.popover("Month"):
                    selected_months = st.multiselect("Select months", months)
    
            # quarter filter
            
            with quarter_col:
                with st.popover("Quarter"):
                    selected_quarters = st.multiselect("Select quarters", [1, 2, 3, 4])
    
        st.subheader("")
        st.divider()
        st.subheader("")
    
        # kpi cards
    
        if selected_years:
            selected_year = selected_years[0]
            previous_year = selected_year - 1
    
            current_data = df1[df1["year"] == selected_year]
            previous_data = df1[df1["year"] == previous_year]
    
            revenue = current_data["revenue"].sum()
            previous_revenue = previous_data["revenue"].sum()
            profit = current_data["profit"].sum()
            previous_profit = previous_data["profit"].sum()
            number_of_orders = current_data["order_id"].nunique()
            previous_number_of_orders = previous_data["order_id"].nunique()
    
            revenue_delta = revenue - previous_revenue
            profit_delta = profit - previous_profit
            orders_delta = number_of_orders - previous_number_of_orders
    
            sp1, kpi1, sp2, kpi2, sp3, kpi3, sp4 = st.columns(7)
    
            with kpi1:
                st.metric(label="💰 Revenue", value=f"${revenue:,.0f}", delta=f"${revenue_delta:+,.0f} vs {previous_year}")
    
            with kpi2:
                st.metric(label="💵 Profit", value=f"${profit:,.0f}", delta=f"${profit_delta:+,.0f} vs {previous_year}")
    
            with kpi3:
                st.metric(label="🛒 Number of Orders", value=f"{number_of_orders:,}", delta=f"{orders_delta:+,} vs {previous_year}")




    
    # geographic analysis
    
    elif page_analysis == 3:
        st.header("Geographic Analysis 🌍")
    
    
    # product analysis
    
    elif page_analysis == 4:
        st.header("Product Analysis 🏷️")
