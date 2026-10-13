# import librairies

import streamlit as st
import pandas as pd
import altair as alt

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

    sp1, sp2, pagination_col, sp4, sp5 = st.columns(5)

    with pagination_col:
        page_analysis = st.pagination(4)

    st.subheader("")

    # dataset overview

    if page_analysis == 1:

        st.header("Data Overview 📁")

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

        # prepare data

        df1["order_date"] = pd.to_datetime(df1["order_date"])
        df1["year"] = df1["order_date"].dt.year
        df1["month"] = df1["order_date"].dt.month
        df1["month_name"] = df1["order_date"].dt.strftime("%B")
        df1["quarter"] = df1["order_date"].dt.quarter

        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]

        # header and filters

        title_col, sp6, filters_col = st.columns([3, 1, 4])

        with title_col:
            st.header("Business Performance Over Time 📊")

        with filters_col:
            st.markdown("**Filters**")
            year_col, month_col, quarter_col = st.columns(3)

            with year_col:
                with st.popover("Year"):
                    available_years = sorted(df1["year"].unique(), reverse=True)
                    default_years = [year for year in [2025, 2024] if year in available_years]

                    selected_years = st.multiselect(
                        "Select years",
                        available_years,
                        default=default_years
                    )

            with month_col:
                with st.popover("Month"):
                    selected_months = st.multiselect("Select months", months)

            with quarter_col:
                with st.popover("Quarter"):
                    selected_quarters = st.multiselect("Select quarters", [1, 2, 3, 4])

        st.divider()

        # apply filters

        if selected_years:

            chart_data = df1[df1["year"].isin(selected_years)].copy()

            if selected_months:
                chart_data = chart_data[chart_data["month_name"].isin(selected_months)]

            if selected_quarters:
                chart_data = chart_data[chart_data["quarter"].isin(selected_quarters)]

            # kpi calculations

            revenue = chart_data["revenue"].sum()
            profit = chart_data["profit"].sum()
            number_of_orders = chart_data["order_id"].nunique()
            total_costs = chart_data["cost"].sum()

            # compare the two most recent selected years when applicable

            comparison_years = sorted(selected_years, reverse=True)
            revenue_delta = None
            profit_delta = None
            orders_delta = None

            if len(comparison_years) == 2:

                current_year = comparison_years[0]
                previous_year = comparison_years[1]

                current_data = chart_data[chart_data["year"] == current_year]
                previous_data = chart_data[chart_data["year"] == previous_year]

                current_revenue = current_data["revenue"].sum()
                previous_revenue = previous_data["revenue"].sum()

                current_profit = current_data["profit"].sum()
                previous_profit = previous_data["profit"].sum()

                current_orders = current_data["order_id"].nunique()
                previous_orders = previous_data["order_id"].nunique()

                revenue_delta = (
                    (current_revenue - previous_revenue) / previous_revenue * 100
                    if previous_revenue != 0 else None
                )

                profit_delta = (
                    (current_profit - previous_profit) / previous_profit * 100
                    if previous_profit != 0 else None
                )

                orders_delta = (
                    (current_orders - previous_orders) / previous_orders * 100
                    if previous_orders != 0 else None
                )

            # kpi sidebar

            kpi_col, sp7, charts_col = st.columns([1.2, 0.1, 4.5])

            with kpi_col:

                st.subheader("Key Metrics")
                st.header("")

                st.metric(
                    "💰 Revenue",
                    f"${revenue:,.0f}",
                    delta=f"{revenue_delta:+.1f}%" if revenue_delta is not None else None
                )
                
                st.header("")

                st.metric(
                    "📈 Profit",
                    f"${profit:,.0f}",
                    delta=f"{profit_delta:+.1f}%" if profit_delta is not None else None
                )
                
                st.header("")

                st.metric(
                    "🛒 Number of Orders",
                    f"{number_of_orders:,}",
                    delta=f"{orders_delta:+.1f}%" if orders_delta is not None else None
                )
                
                st.header("")

                st.metric("💸 Total Costs", f"${total_costs:,.0f}")

            # prepare chart data

            chart_data["year"] = chart_data["year"].astype(str)

            # dynamic year colors

            sorted_years = sorted(selected_years)

            color_palette = [
                "#0868C9",
                "#F28E2B",
                "#2CA02C",
                "#9467BD",
                "#D62728",
                "#17BECF"
            ]

            year_colors = alt.Scale(
                domain=[str(year) for year in sorted_years],
                range=[
                    color_palette[i % len(color_palette)]
                    for i in range(len(sorted_years))
                ]
            )

            # line chart

            with charts_col:

                st.subheader("Monthly Revenue Comparison")
                st.caption("")

                monthly_revenue = chart_data.groupby(
                    ["year", "month", "month_name"]
                )["revenue"].sum().reset_index()

                monthly_revenue = monthly_revenue.rename(
                    columns={"month_name": "Month", "revenue": "Revenue"}
                )

                # dynamic Y-axis range for revenue

                revenue_min = monthly_revenue["Revenue"].min()
                revenue_max = monthly_revenue["Revenue"].max()
                revenue_padding = (revenue_max - revenue_min) * 0.15

                if revenue_padding == 0:
                    revenue_padding = revenue_max * 0.05 if revenue_max != 0 else 1

                revenue_chart = alt.Chart(monthly_revenue).mark_line(
                    point=True
                ).encode(
                    x=alt.X("Month:N", sort=months, title="Month"),
                    y=alt.Y(
                        "Revenue:Q",
                        axis=alt.Axis(format="$,.0f"),
                        title="Revenue",
                        scale=alt.Scale(
                            domain=[
                                max(0, revenue_min - revenue_padding),
                                revenue_max + revenue_padding
                            ],
                            zero=False
                        )
                    ),
                    color=alt.Color(
                        "year:N",
                        title="Year",
                        scale=year_colors
                    ),
                    tooltip=[
                        alt.Tooltip("year:N", title="Year"),
                        alt.Tooltip("Month:N", title="Month"),
                        alt.Tooltip(
                            "Revenue:Q",
                            title="Revenue",
                            format="$,.0f"
                        )
                    ]
                ).properties(height=350)

                st.altair_chart(revenue_chart, width="stretch")

                st.divider()

                # bottom charts

                profit_col, sp8, quarter_col = st.columns([1, 0.3, 1])

                # profit chart

                with profit_col:

                    st.subheader("Monthly Profit Comparison")
                    st.caption("")

                    monthly_profit = chart_data.groupby(
                        ["year", "month", "month_name"]
                    )["profit"].sum().reset_index()

                    monthly_profit = monthly_profit.rename(
                        columns={"month_name": "Month", "profit": "Profit"}
                    )

                    # dynamic Y-axis range for profit

                    profit_min = monthly_profit["Profit"].min()
                    profit_max = monthly_profit["Profit"].max()
                    profit_padding = (profit_max - profit_min) * 0.15

                    if profit_padding == 0:
                        profit_padding = profit_max * 0.05 if profit_max != 0 else 1

                    profit_chart = alt.Chart(monthly_profit).mark_line(
                        point=True
                    ).encode(
                        x=alt.X("Month:N", sort=months, title="Month"),
                        y=alt.Y(
                            "Profit:Q",
                            axis=alt.Axis(format="$,.0f"),
                            title="Profit",
                            scale=alt.Scale(
                                domain=[
                                    max(0, profit_min - profit_padding),
                                    profit_max + profit_padding
                                ],
                                zero=False
                            )
                        ),
                        color=alt.Color(
                            "year:N",
                            title="Year",
                            scale=year_colors
                        ),
                        tooltip=[
                            alt.Tooltip("year:N", title="Year"),
                            alt.Tooltip("Month:N", title="Month"),
                            alt.Tooltip(
                                "Profit:Q",
                                title="Profit",
                                format="$,.0f"
                            )
                        ]
                    ).properties(height=300)

                    st.altair_chart(profit_chart, width="stretch")

                # bar chart

                with quarter_col:

                    st.subheader("Quarterly Revenue Comparison")
                    st.caption("")

                    quarterly_revenue = chart_data.groupby(
                        ["year", "quarter"]
                    )["revenue"].sum().reset_index()

                    quarterly_revenue["Quarter"] = (
                        "Q" + quarterly_revenue["quarter"].astype(str)
                    )

                    quarter_chart = alt.Chart(quarterly_revenue).mark_bar(
                        cornerRadiusTopLeft=4,
                        cornerRadiusTopRight=4
                    ).encode(
                        x=alt.X(
                            "Quarter:N",
                            sort=["Q1", "Q2", "Q3", "Q4"],
                            title="Quarter"
                        ),
                        y=alt.Y(
                            "revenue:Q",
                            axis=alt.Axis(format="$,.0f"),
                            title="Revenue",
                            scale=alt.Scale(zero=True)
                        ),
                        color=alt.Color(
                            "year:N",
                            title="Year",
                            scale=year_colors
                        ),
                        xOffset="year:N",
                        tooltip=[
                            alt.Tooltip("year:N", title="Year"),
                            alt.Tooltip("Quarter:N", title="Quarter"),
                            alt.Tooltip(
                                "revenue:Q",
                                title="Revenue",
                                format="$,.0f"
                            )
                        ]
                    ).properties(height=300)

                    st.altair_chart(quarter_chart, width="stretch")

            st.divider()

        else:
            st.info("Please select at least one year to display the analysis.")
    

    

##########################################################################################

    
    
    # product sales analysis

    elif page_analysis == 3:
        
        st.header("Product Sales Analysis 🛍️")

        st.subheader("")

        st.divider()
    
        # aggregate revenue by category
    
        category_sales = (
            df1.groupby("category", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
        )
    
        # calculate revenue share
    
        total_revenue = category_sales["revenue"].sum()
    
        category_sales["revenue_share"] = (
            category_sales["revenue"] / total_revenue
            if total_revenue != 0
            else 0
        )
    
        # aggregate units sold by category
    
        category_quantity = (
            df1.groupby("category", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
        )
    
        # aggregate revenue by product and select top 5
    
        top_products = (
            df1.groupby("product", as_index=False)["revenue"]
            .sum()
            .nlargest(5, "revenue")
            .sort_values("revenue", ascending=True)
        )
    
        # create chart layout
    
        bar_col, donut_col = st.columns(2)
    
        # sales by category
    
        with bar_col:
            st.subheader("Sales by Category")
    
            category_bars = (
                alt.Chart(category_sales)
                .mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5
                )
                .encode(
                    x=alt.X(
                        "category:N",
                        title=None,
                        sort="-y",
                        axis=alt.Axis(labelAngle=0)
                    ),
                    y=alt.Y(
                        "revenue:Q",
                        title="Revenue",
                        axis=alt.Axis(format=",.0f"),
                        scale=alt.Scale(zero=True)
                    ),
                    color=alt.Color(
                        "category:N",
                        legend=None,
                        scale=alt.Scale(scheme="tableau10")
                    ),
                    tooltip=[
                        alt.Tooltip("category:N", title="Category"),
                        alt.Tooltip(
                            "revenue:Q",
                            title="Revenue",
                            format=",.2f"
                        )
                    ]
                )
            )
    
            category_labels = (
                alt.Chart(category_sales)
                .mark_text(
                    dy=-8,
                    fontSize=11
                )
                .encode(
                    x=alt.X("category:N", sort="-y"),
                    y=alt.Y("revenue:Q"),
                    text=alt.Text("revenue:Q", format=",.0f")
                )
            )
    
            category_chart = (
                (category_bars + category_labels)
                .properties(height=350)
            )
    
            st.altair_chart(
                category_chart,
                use_container_width=True
            )
    
        # sales distribution
    
        with donut_col:
            st.subheader("Sales Distribution")
    
            donut_base = alt.Chart(category_sales)
    
            donut_chart = (
                donut_base
                .mark_arc(
                    innerRadius=65,
                    outerRadius=115,
                    cornerRadius=3
                )
                .encode(
                    theta=alt.Theta(
                        "revenue:Q",
                        stack=True
                    ),
                    color=alt.Color(
                        "category:N",
                        title="Category",
                        scale=alt.Scale(scheme="tableau10")
                    ),
                    order=alt.Order(
                        "revenue:Q",
                        sort="descending"
                    ),
                    tooltip=[
                        alt.Tooltip("category:N", title="Category"),
                        alt.Tooltip(
                            "revenue:Q",
                            title="Revenue",
                            format=",.2f"
                        ),
                        alt.Tooltip(
                            "revenue_share:Q",
                            title="Revenue Share",
                            format=".1%"
                        )
                    ]
                )
            )
    
            donut_labels = (
                donut_base
                .transform_filter(
                    alt.datum.revenue_share >= 0.05
                )
                .mark_text(
                    radius=92,
                    fontSize=11,
                    fontWeight="bold",
                    color="white"
                )
                .encode(
                    theta=alt.Theta(
                        "revenue:Q",
                        stack=True
                    ),
                    order=alt.Order(
                        "revenue:Q",
                        sort="descending"
                    ),
                    text=alt.Text(
                        "revenue_share:Q",
                        format=".1%"
                    )
                )
            )
    
            donut = (
                (donut_chart + donut_labels)
                .properties(height=350)
            )
    
            st.altair_chart(
                donut,
                use_container_width=True
            )
    
        # add spacing between chart rows
    
        st.write("")
    
        top_col, quantity_col = st.columns(2)
    
        # top 5 products by revenue
    
        with top_col:
            st.subheader("Top 5 Products by Revenue")
    
            top_products_chart = (
                alt.Chart(top_products)
                .mark_bar(
                    cornerRadiusEnd=5,
                    color="#4C78A8"
                )
                .encode(
                    y=alt.Y(
                        "product:N",
                        title=None,
                        sort="-x"
                    ),
                    x=alt.X(
                        "revenue:Q",
                        title="Revenue",
                        axis=alt.Axis(format=",.0f"),
                        scale=alt.Scale(zero=True)
                    ),
                    tooltip=[
                        alt.Tooltip("product:N", title="Product"),
                        alt.Tooltip(
                            "revenue:Q",
                            title="Revenue",
                            format=",.2f"
                        )
                    ]
                )
            )
    
            top_products_labels = (
                alt.Chart(top_products)
                .mark_text(
                    align="left",
                    dx=5,
                    fontSize=11
                )
                .encode(
                    y=alt.Y("product:N", sort="-x"),
                    x=alt.X("revenue:Q"),
                    text=alt.Text("revenue:Q", format=",.0f")
                )
            )
    
            top_products_chart = (
                (top_products_chart + top_products_labels)
                .properties(height=350)
            )
    
            st.altair_chart(
                top_products_chart,
                use_container_width=True
            )
    
        # units sold by category
    
        with quantity_col:
            st.subheader("Units Sold by Category")
    
            quantity_bars = (
                alt.Chart(category_quantity)
                .mark_bar(
                    cornerRadiusTopLeft=5,
                    cornerRadiusTopRight=5,
                    color="#59A14F"
                )
                .encode(
                    x=alt.X(
                        "category:N",
                        title=None,
                        sort="-y",
                        axis=alt.Axis(labelAngle=0)
                    ),
                    y=alt.Y(
                        "quantity:Q",
                        title="Units Sold",
                        axis=alt.Axis(format=",.0f"),
                        scale=alt.Scale(zero=True)
                    ),
                    tooltip=[
                        alt.Tooltip("category:N", title="Category"),
                        alt.Tooltip(
                            "quantity:Q",
                            title="Units Sold",
                            format=",.0f"
                        )
                    ]
                )
            )
    
            quantity_labels = (
                alt.Chart(category_quantity)
                .mark_text(
                    dy=-8,
                    fontSize=11
                )
                .encode(
                    x=alt.X("category:N", sort="-y"),
                    y=alt.Y("quantity:Q"),
                    text=alt.Text("quantity:Q", format=",.0f")
                )
            )
    
            quantity_chart = (
                (quantity_bars + quantity_labels)
                .properties(height=350)
            )
    
            st.altair_chart(
                quantity_chart,
                use_container_width=True
            )

    
    # geographic analysis
    
    elif page_analysis == 4:
        st.header("Geographic Analysis 🗺️")
