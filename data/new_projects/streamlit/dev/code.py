# imports

import streamlit as st
import pandas as pd
import altair as alt
from streamviz import gauge

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


    
##########################################################################################

    
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

        h1, sp6, f1 = st.columns([3, 1, 4])

        with h1:
            st.header("Business Performance Over Time 📊")

        with f1:
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

                st.markdown("**Key Metrics**")
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

                st.markdown("**Monthly Revenue Comparison**")
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

                    st.markdown("**Monthly Profit Comparison**")
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

                    st.markdown("**Quarterly Revenue Comparison**")
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


    elif page_analysis == 3:

        # header & filters space

        h2, sp9, f2, sp10, f3 = st.columns([4, 0.2, 1, 0.2, 1])

        with h2:
            st.header("Product Sales Analysis 🛍️")

        with f2:
            selected_category = st.selectbox(
                "Category",
                options=["All"] + sorted(df1["category"].dropna().unique().tolist()),
                index=0
            )

        with f3:
            selected_channel = st.selectbox(
                "Sales Channel",
                options=["All"] + sorted(df1["sales_channel"].dropna().unique().tolist()),
                index=0
            )

        st.subheader("")
        st.divider()

        # filter the dataset

        filtered_df = df1.copy()

        if selected_category != "All":
            filtered_df = filtered_df[
                filtered_df["category"] == selected_category
            ]

        if selected_channel != "All":
            filtered_df = filtered_df[
                filtered_df["sales_channel"] == selected_channel
            ]

        # calculate the selected metrics

        units_sold = filtered_df["quantity"].sum()
        total_revenue = filtered_df["revenue"].sum()
        total_profit = filtered_df["profit"].sum()

        # calculate gauge ranges

        combination_totals = (
            df1.groupby(["category", "sales_channel"])[
                ["quantity", "revenue", "profit"]
            ].sum()
        )

        max_units = max(combination_totals["quantity"].max(), 3000)
        max_revenue = max(combination_totals["revenue"].max(), 1)
        max_profit = max(combination_totals["profit"].max(), 1)

        
        # create the three gauges

        g1, s11, g2, s12, g3 = st.columns([1, 0.3, 1, 0.3, 1])

        # display the units sold circular gauge

        with g1:

            units_gauge_options = {
                "animation": True,
                "series": [{
                    "type": "gauge",
                    "startAngle": 90,
                    "endAngle": -270,
                    "min": 0,
                    "max": float(max(max_units, units_sold, 1)),
                    "progress": {
                        "show": True,
                        "width": 16,
                        "roundCap": True,
                        "itemStyle": {"color": "#4387C5"}
                    },
                    "axisLine": {
                        "roundCap": True,
                        "lineStyle": {
                            "width": 16,
                            "color": [[1, "#E8EDF3"]]
                        }
                    },
                    "pointer": {"show": False},
                    "axisTick": {"show": False},
                    "splitLine": {"show": False},
                    "axisLabel": {"show": False},
                    "title": {
                        "show": True,
                        "offsetCenter": [0, "32%"],
                        "fontSize": 13,
                        "color": "#64748B"
                    },
                    "detail": {
                        "valueAnimation": True,
                        "offsetCenter": [0, "-5%"],
                        "fontSize": 23,
                        "fontWeight": "bold",
                        "color": "#4387C5",
                        "formatter": "{value}"
                    },
                    "data": [{
                        "value": int(units_sold),
                        "name": "Units Sold"
                    }]
                }]
            }

            st.echarts_chart(
                units_gauge_options,
                height=250,
                key="sales_units_circular_gauge"
            )

        # display the revenue circular gauge

        with g2:

            revenue_max = max(max_revenue, total_revenue, 1)

            revenue_gauge_options = {
                "animation": True,
                "series": [{
                    "type": "gauge",
                    "startAngle": 90,
                    "endAngle": -270,
                    "min": 0,
                    "max": float(revenue_max),
                    "progress": {
                        "show": True,
                        "width": 16,
                        "roundCap": True,
                        "itemStyle": {"color": "#8E63CE"}
                    },
                    "axisLine": {
                        "roundCap": True,
                        "lineStyle": {
                            "width": 16,
                            "color": [[1, "#E8EDF3"]]
                        }
                    },
                    "pointer": {"show": False},
                    "axisTick": {"show": False},
                    "splitLine": {"show": False},
                    "axisLabel": {"show": False},
                    "title": {
                        "show": True,
                        "offsetCenter": [0, "32%"],
                        "fontSize": 13,
                        "color": "#64748B"
                    },
                    "detail": {
                        "valueAnimation": True,
                        "offsetCenter": [0, "-5%"],
                        "fontSize": 19,
                        "fontWeight": "bold",
                        "color": "#8E63CE",
                        "formatter": "${value}"
                    },
                    "data": [{
                        "value": float(total_revenue),
                        "name": "Revenue ($)"
                    }]
                }]
            }

            st.echarts_chart(
                revenue_gauge_options,
                height=250,
                key="sales_revenue_circular_gauge"
            )

        # display the profit circular gauge

        with g3:

            profit_max = max(max_profit, total_profit, 1)

            profit_gauge_options = {
                "animation": True,
                "series": [{
                    "type": "gauge",
                    "startAngle": 90,
                    "endAngle": -270,
                    "min": 0,
                    "max": float(profit_max),
                    "progress": {
                        "show": True,
                        "width": 16,
                        "roundCap": True,
                        "itemStyle": {"color": "#2E8B57"}
                    },
                    "axisLine": {
                        "roundCap": True,
                        "lineStyle": {
                            "width": 16,
                            "color": [[1, "#E8EDF3"]]
                        }
                    },
                    "pointer": {"show": False},
                    "axisTick": {"show": False},
                    "splitLine": {"show": False},
                    "axisLabel": {"show": False},
                    "title": {
                        "show": True,
                        "offsetCenter": [0, "32%"],
                        "fontSize": 13,
                        "color": "#64748B"
                    },
                    "detail": {
                        "valueAnimation": True,
                        "offsetCenter": [0, "-5%"],
                        "fontSize": 19,
                        "fontWeight": "bold",
                        "color": "#2E8B57",
                        "formatter": "${value}"
                    },
                    "data": [{
                        "value": float(total_profit),
                        "name": "Profit ($)"
                    }]
                }]
            }

            st.echarts_chart(
                profit_gauge_options,
                height=250,
                key="sales_profit_circular_gauge"
            )


        # prepare the top five products by units sold

        product_units = (
            filtered_df.groupby("product", as_index=False)["quantity"]
            .sum()
            .nlargest(5, "quantity")
            .sort_values("quantity", ascending=True)
        )

        # prepare the top five products by profit

        product_profit = (
            filtered_df.groupby("product", as_index=False)["profit"]
            .sum()
            .nlargest(5, "profit")
            .sort_values("profit", ascending=True)
        )

        # aggregate revenue by sales channel

        channel_performance = (
            filtered_df.groupby("sales_channel", as_index=False)
            .agg(Revenue=("revenue", "sum"))
            .sort_values("Revenue", ascending=False)
        )

        # create the chart columns

        st.subheader("Product & Channel Performance")

        c1, s13, c2, s14, c3 = st.columns([1, 0.3, 1, 0.3, 1])

        with c1:

            st.markdown("**Top 5 Products by Units Sold**")

            units_options = {
                "animation": True,
                "grid": {
                    "left": 8,
                    "right": 18,
                    "top": 15,
                    "bottom": 35,
                    "containLabel": True
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"},
                    "valueFormatter": "{value}"
                },
                "xAxis": {
                    "type": "value",
                    "name": "Units Sold",
                    "nameLocation": "middle",
                    "nameGap": 25,
                    "min": 0,
                    "axisLabel": {"show": True}
                },
                "yAxis": {
                    "type": "category",
                    "data": product_units["product"].tolist(),
                    "axisLabel": {"width": 100, "overflow": "truncate"}
                },
                "series": [{
                    "name": "Units Sold",
                    "type": "bar",
                    "data": product_units["quantity"].tolist(),
                    "barMaxWidth": 28,
                    "itemStyle": {
                        "color": "#4387C5",
                        "borderRadius": [0, 5, 5, 0]
                    },
                    "label": {
                        "show": True,
                        "position": "right",
                        "color": "#4387C5"
                    }
                }]
            }

            st.echarts_chart(
                units_options,
                height=300,
                key="product_units_echart"
            )

        with c2:

            st.markdown("**Top 5 Products by Profit**")

            profit_options = {
                "animation": True,
                "grid": {
                    "left": 8,
                    "right": 25,
                    "top": 15,
                    "bottom": 35,
                    "containLabel": True
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"}
                },
                "xAxis": {
                    "type": "value",
                    "name": "Profit ($)",
                    "nameLocation": "middle",
                    "nameGap": 25,
                    "min": 0,
                    "axisLabel": {"show": True}
                },
                "yAxis": {
                    "type": "category",
                    "data": product_profit["product"].tolist(),
                    "axisLabel": {"width": 100, "overflow": "truncate"}
                },
                "series": [{
                    "name": "Profit ($)",
                    "type": "bar",
                    "data": product_profit["profit"].tolist(),
                    "barMaxWidth": 28,
                    "itemStyle": {
                        "color": "#8E63CE",
                        "borderRadius": [0, 5, 5, 0]
                    },
                    "label": {
                        "show": True,
                        "position": "right",
                        "color": "#8E63CE",
                        "formatter": "{c}"
                    }
                }]
            }

            st.echarts_chart(
                profit_options,
                height=300,
                key="product_profit_echart"
            )

        with c3:

            st.markdown("**Revenue Share by Channel**")

            channel_options = {
                "animation": True,
                "color": ["#4387C5", "#FB8C00", "#8E63CE", "#2E8B57"],
                "tooltip": {
                    "trigger": "item",
                    "formatter": "{b}<br/>Revenue: ${c}<br/>Share: {d}%"
                },
                "legend": {
                    "orient": "horizontal",
                    "bottom": 0,
                    "left": "center"
                },
                "series": [{
                    "name": "Revenue",
                    "type": "pie",
                    "radius": ["38%", "68%"],
                    "center": ["50%", "44%"],
                    "avoidLabelOverlap": True,
                    "itemStyle": {
                        "borderColor": "#FFFFFF",
                        "borderWidth": 2
                    },
                    "label": {
                        "show": True,
                        "formatter": "{d}%",
                        "fontSize": 12
                    },
                    "labelLine": {
                        "show": True
                    },
                    "data": [
                        {
                            "name": row["sales_channel"],
                            "value": float(row["Revenue"])
                        }
                        for _, row in channel_performance.iterrows()
                    ]
                }]
            }

            st.echarts_chart(
                channel_options,
                height=300,
                key="channel_revenue_echart"
            )

        # create the dashboard footer section

        st.subheader("")
        st.divider()



    
    # geographic analysis
        
    elif page_analysis == 4:
    

