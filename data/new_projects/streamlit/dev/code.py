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

        # prepare date fields

        df1["order_date"] = pd.to_datetime(df1["order_date"])
        df1["year"] = df1["order_date"].dt.year
        df1["month"] = df1["order_date"].dt.month
        df1["month_name"] = df1["order_date"].dt.strftime("%B")
        df1["quarter"] = df1["order_date"].dt.quarter

        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        # header and filters

        h1, sp6, f1 = st.columns([3, 1, 4])

        with h1:
            st.header("Business Performance Over Time 📊")

        with f1:
            st.markdown("**Filters**")
            year_col, month_col, quarter_col = st.columns(3)

            with year_col:
                with st.popover("Year"):
                    available_years = sorted(
                        [int(year) for year in df1["year"].dropna().unique()],
                        reverse=True
                    )

                    default_years = [
                        year for year in [2025, 2024]
                        if year in available_years
                    ]

                    selected_years = st.multiselect(
                        "Select years",
                        available_years,
                        default=default_years
                    )

            with month_col:
                with st.popover("Month"):
                    selected_months = st.multiselect(
                        "Select months",
                        months
                    )

            with quarter_col:
                with st.popover("Quarter"):
                    selected_quarters = st.multiselect(
                        "Select quarters",
                        [1, 2, 3, 4]
                    )

        st.divider()

        if selected_years:

            # apply filters

            chart_data = df1[
                df1["year"].isin(selected_years)
            ].copy()

            if selected_months:
                chart_data = chart_data[
                    chart_data["month_name"].isin(selected_months)
                ]

            if selected_quarters:
                chart_data = chart_data[
                    chart_data["quarter"].isin(selected_quarters)
                ]

            # calculate key metrics

            revenue = float(chart_data["revenue"].sum())
            profit = float(chart_data["profit"].sum())
            number_of_orders = int(chart_data["order_id"].nunique())
            total_costs = float(chart_data["cost"].sum())

            # calculate comparison metrics

            revenue_delta = None
            profit_delta = None
            orders_delta = None
            costs_delta = None

            if len(selected_years) == 1 and int(selected_years[0]) == 2025:

                comparison_data = df1[df1["year"] == 2024].copy()

                if selected_months:
                    comparison_data = comparison_data[
                        comparison_data["month_name"].isin(selected_months)
                    ]

                if selected_quarters:
                    comparison_data = comparison_data[
                        comparison_data["quarter"].isin(selected_quarters)
                    ]

                previous_revenue = float(comparison_data["revenue"].sum())
                previous_profit = float(comparison_data["profit"].sum())
                previous_orders = int(comparison_data["order_id"].nunique())
                previous_costs = float(comparison_data["cost"].sum())

                revenue_delta = (
                    (revenue - previous_revenue) / abs(previous_revenue) * 100
                    if previous_revenue != 0 else None
                )

                profit_delta = (
                    (profit - previous_profit) / abs(previous_profit) * 100
                    if previous_profit != 0 else None
                )

                orders_delta = (
                    (number_of_orders - previous_orders) / abs(previous_orders) * 100
                    if previous_orders != 0 else None
                )

                costs_delta = (
                    (total_costs - previous_costs) / abs(previous_costs) * 100
                    if previous_costs != 0 else None
                )

            # prepare the layout

            kpi_col, sp7, charts_col = st.columns([1.2, 0.1, 4.5])

            with kpi_col:

                st.markdown("**Key Metrics**")

                # calculate visual progress values

                metric_values = [
                    revenue,
                    profit,
                    number_of_orders,
                    total_costs
                ]

                metric_maxima = [
                    max(abs(value) for value in metric_values) or 1,
                    max(abs(value) for value in metric_values) or 1,
                    max(abs(value) for value in metric_values) or 1,
                    max(abs(value) for value in metric_values) or 1
                ]

                metric_cards = [
                    {
                        "title": "Revenue",
                        "value": f"${revenue:,.0f}",
                        "delta": revenue_delta,
                        "color": "#4387C5",
                        "progress": 100 * abs(revenue) / metric_maxima[0]
                    },
                    {
                        "title": "Profit",
                        "value": f"${profit:,.0f}",
                        "delta": profit_delta,
                        "color": "#8E63CE",
                        "progress": 100 * abs(profit) / metric_maxima[1]
                    },
                    {
                        "title": "Number of Orders",
                        "value": f"{number_of_orders:,}",
                        "delta": orders_delta,
                        "color": "#FB8C00",
                        "progress": 100 * abs(number_of_orders) / metric_maxima[2]
                    },
                    {
                        "title": "Total Costs",
                        "value": f"${total_costs:,.0f}",
                        "delta": costs_delta,
                        "color": "#2E8B57",
                        "progress": 100 * abs(total_costs) / metric_maxima[3]
                    }
                ]

                for i, metric in enumerate(metric_cards):

                    with st.container(border=True):

                        st.markdown(
                            f"<span style='color:{metric['color']};font-weight:600'>"
                            f"{metric['title']}</span>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<h3 style='margin:0;color:{metric['color']}'>"
                            f"{metric['value']}</h3>",
                            unsafe_allow_html=True
                        )

                        if metric["delta"] is not None:

                            delta_color = (
                                "#2E8B57"
                                if metric["delta"] >= 0
                                else "#E53935"
                            )

                            st.markdown(
                                f"<span style='color:{delta_color};font-size:12px'>"
                                f"{metric['delta']:+.1f}% vs previous year</span>",
                                unsafe_allow_html=True
                            )

                        st.progress(
                            min(1.0, max(0.0, float(metric["progress"]) / 100))
                        )

            # prepare year colors

            sorted_years = sorted(
                [int(year) for year in selected_years]
            )

            color_palette = [
                "#0868C9",
                "#F28E2B",
                "#2CA02C",
                "#9467BD",
                "#D62728",
                "#17BECF"
            ]

            year_color_map = {
                year: color_palette[i % len(color_palette)]
                for i, year in enumerate(sorted_years)
            }

            # prepare monthly and quarterly data

            monthly_revenue = (
                chart_data.groupby(["year", "month"], as_index=False)["revenue"]
                .sum()
            )

            monthly_profit = (
                chart_data.groupby(["year", "month"], as_index=False)["profit"]
                .sum()
            )

            quarterly_revenue = (
                chart_data.groupby(["year", "quarter"], as_index=False)["revenue"]
                .sum()
            )

            # create the chart layout

            with charts_col:

                st.markdown("**Monthly Revenue Comparison**")

                # configure monthly revenue series

                revenue_series = []

                for year in sorted_years:

                    year_data = monthly_revenue[
                        monthly_revenue["year"] == year
                    ].set_index("month")

                    revenue_values = [
                        (
                            int(round(float(year_data.loc[month, "revenue"]) / 1000))
                            if month in year_data.index else None
                        )
                        for month in range(1, 13)
                    ]

                    revenue_series.append({
                        "name": str(year),
                        "type": "line",
                        "smooth": True,
                        "showSymbol": True,
                        "symbol": "circle",
                        "symbolSize": 6,
                        "connectNulls": False,
                        "data": revenue_values,
                        "itemStyle": {"color": year_color_map[year]},
                        "lineStyle": {"width": 2.5},
                        "emphasis": {"focus": "series"}
                    })

                # configure the monthly revenue chart

                revenue_options = {
                    "animation": True,
                    "grid": {
                        "left": 55,
                        "right": 30,
                        "top": 45,
                        "bottom": 70,
                        "containLabel": True
                    },
                    "tooltip": {
                        "trigger": "axis",
                        "confine": True,
                        "axisPointer": {"type": "line"},
                        "formatter": "{b0}<br/>{a0}: ${c0}K<br/>{a1}: ${c1}K"
                    },
                    "legend": {
                        "data": [str(year) for year in sorted_years],
                        "top": 0,
                        "right": 0
                    },
                    "xAxis": {
                        "type": "category",
                        "boundaryGap": False,
                        "data": months,
                        "name": "Month",
                        "nameLocation": "middle",
                        "nameGap": 38,
                        "axisLabel": {"rotate": 45, "fontSize": 10}
                    },
                    "yAxis": {
                        "type": "value",
                        "min": 0,
                        "name": "Revenue ($K)",
                        "axisLabel": {"formatter": "${value}K"},
                        "splitLine": {
                            "lineStyle": {"color": "#E8EDF3"}
                        }
                    },
                    "series": revenue_series
                }

                st.echarts_chart(
                    revenue_options,
                    height=350,
                    key="monthly_revenue_echart"
                )

                st.divider()

                # create the two bottom charts

                profit_col, sp8, quarter_col = st.columns([1, 0.3, 1])

                with profit_col:

                    st.markdown("**Monthly Profit Comparison**")

                    # configure monthly profit series

                    profit_series = []

                    for year in sorted_years:

                        year_data = monthly_profit[
                            monthly_profit["year"] == year
                        ].set_index("month")

                        profit_values = [
                            (
                                int(round(float(year_data.loc[month, "profit"]) / 1000))
                                if month in year_data.index else None
                            )
                            for month in range(1, 13)
                        ]

                        profit_series.append({
                            "name": str(year),
                            "type": "line",
                            "smooth": True,
                            "showSymbol": True,
                            "symbol": "circle",
                            "symbolSize": 5,
                            "connectNulls": False,
                            "data": profit_values,
                            "itemStyle": {"color": year_color_map[year]},
                            "lineStyle": {"width": 2.5},
                            "emphasis": {"focus": "series"}
                        })

                    # configure the monthly profit chart

                    profit_options = {
                        "animation": True,
                        "grid": {
                            "left": 55,
                            "right": 20,
                            "top": 40,
                            "bottom": 70,
                            "containLabel": True
                        },
                        "tooltip": {
                            "trigger": "axis",
                            "confine": True,
                            "axisPointer": {"type": "line"},
                            "formatter": "{b0}<br/>{a0}: ${c0}K<br/>{a1}: ${c1}K"
                        },
                        "legend": {
                            "data": [str(year) for year in sorted_years],
                            "top": 0,
                            "right": 0
                        },
                        "xAxis": {
                            "type": "category",
                            "boundaryGap": False,
                            "data": months,
                            "name": "Month",
                            "nameLocation": "middle",
                            "nameGap": 38,
                            "axisLabel": {"rotate": 45, "fontSize": 9}
                        },
                        "yAxis": {
                            "type": "value",
                            "min": 0,
                            "name": "Profit ($K)",
                            "axisLabel": {"formatter": "${value}K"},
                            "splitLine": {
                                "lineStyle": {"color": "#E8EDF3"}
                            }
                        },
                        "series": profit_series
                    }

                    st.echarts_chart(
                        profit_options,
                        height=300,
                        key="monthly_profit_echart"
                    )

                with quarter_col:

                    st.markdown("**Quarterly Revenue Comparison**")

                    quarter_labels = ["Q1", "Q2", "Q3", "Q4"]

                    # configure quarterly revenue series

                    quarter_series = []

                    for year in sorted_years:

                        year_data = quarterly_revenue[
                            quarterly_revenue["year"] == year
                        ].set_index("quarter")

                        quarter_values = [
                            (
                                int(round(float(year_data.loc[quarter, "revenue"]) / 1000))
                                if quarter in year_data.index else 0
                            )
                            for quarter in [1, 2, 3, 4]
                        ]

                        quarter_series.append({
                            "name": str(year),
                            "type": "bar",
                            "barMaxWidth": 28,
                            "data": quarter_values,
                            "itemStyle": {
                                "color": year_color_map[year],
                                "borderRadius": [4, 4, 0, 0]
                            },
                            "emphasis": {"focus": "series"}
                        })

                    # configure the quarterly revenue chart

                    quarter_options = {
                        "animation": True,
                        "grid": {
                            "left": 55,
                            "right": 20,
                            "top": 40,
                            "bottom": 45,
                            "containLabel": True
                        },
                        "tooltip": {
                            "trigger": "axis",
                            "confine": True,
                            "axisPointer": {"type": "shadow"},
                            "formatter": "{b0}<br/>{a0}: ${c0}K<br/>{a1}: ${c1}K"
                        },
                        "legend": {
                            "data": [str(year) for year in sorted_years],
                            "top": 0,
                            "right": 0
                        },
                        "xAxis": {
                            "type": "category",
                            "data": quarter_labels,
                            "name": "Quarter",
                            "nameLocation": "middle",
                            "nameGap": 28
                        },
                        "yAxis": {
                            "type": "value",
                            "min": 0,
                            "name": "Revenue ($K)",
                            "axisLabel": {"formatter": "${value}K"},
                            "splitLine": {
                                "lineStyle": {"color": "#E8EDF3"}
                            }
                        },
                        "series": quarter_series
                    }

                    st.echarts_chart(
                        quarter_options,
                        height=300,
                        key="quarterly_revenue_echart"
                    )

            st.divider()

        else:
            st.info("Please select at least one year to display the analysis.")



    

##########################################################################################

    # product analysis
    
    
    elif page_analysis == 3:

        # create the header and filter columns

        h2, sp9, f2, sp10, f3 = st.columns([4, 0.2, 1, 0.2, 1])

        with h2:
            st.header("Product Sales Analysis 🛍️")

        with f2:
            selected_category = st.selectbox(
                "Category",
                options=["All"] + sorted(
                    df1["category"].dropna().unique().tolist()
                ),
                index=0
            )

        with f3:
            selected_channel = st.selectbox(
                "Sales Channel",
                options=["All"] + sorted(
                    df1["sales_channel"].dropna().unique().tolist()
                ),
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

        units_sold = int(filtered_df["quantity"].sum())
        total_revenue = float(filtered_df["revenue"].sum())
        total_profit = float(filtered_df["profit"].sum())

        # format the gauge values for display

        units_display = (
            f"{units_sold / 1_000_000:.2f}M"
            if abs(units_sold) >= 1_000_000
            else f"{units_sold / 1_000:.1f}K"
            if abs(units_sold) >= 1_000
            else str(units_sold)
        )

        revenue_display = (
            f"${total_revenue / 1_000_000:.2f}M"
            if abs(total_revenue) >= 1_000_000
            else f"${total_revenue / 1_000:.1f}K"
            if abs(total_revenue) >= 1_000
            else f"${total_revenue:.0f}"
        )

        profit_display = (
            f"${total_profit / 1_000_000:.2f}M"
            if abs(total_profit) >= 1_000_000
            else f"${total_profit / 1_000:.1f}K"
            if abs(total_profit) >= 1_000
            else f"${total_profit:.0f}"
        )

        # set fixed gauge ranges

        max_units = 30000
        max_revenue = 5000000
        max_profit = 2000000

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
                    "max": max_units,
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
                        "fontSize": 22,
                        "fontWeight": "bold",
                        "color": "#4387C5",
                        "formatter": units_display
                    },
                    "data": [{
                        "value": units_sold,
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

            revenue_gauge_options = {
                "animation": True,
                "series": [{
                    "type": "gauge",
                    "startAngle": 90,
                    "endAngle": -270,
                    "min": 0,
                    "max": max_revenue,
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
                        "fontSize": 17,
                        "fontWeight": "bold",
                        "color": "#8E63CE",
                        "formatter": revenue_display
                    },
                    "data": [{
                        "value": total_revenue,
                        "name": "Revenue"
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

            profit_gauge_options = {
                "animation": True,
                "series": [{
                    "type": "gauge",
                    "startAngle": 90,
                    "endAngle": -270,
                    "min": 0,
                    "max": max_profit,
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
                        "fontSize": 17,
                        "fontWeight": "bold",
                        "color": "#2E8B57",
                        "formatter": profit_display
                    },
                    "data": [{
                        "value": total_profit,
                        "name": "Profit"
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

        # aggregate revenue across all sales channels

        channel_performance = (
            df1.groupby("sales_channel", as_index=False)
            .agg(Revenue=("revenue", "sum"))
            .sort_values("Revenue", ascending=False)
        )

        st.subheader("")

        # create the chart columns

        c1, s13, c2, s14, c3 = st.columns([1, 0.3, 1, 0.3, 1])

        with c1:

            st.markdown("**Top 5 Products by Units Sold**")

            units_options = {
                "animation": True,
                "grid": {
                    "left": 8,
                    "right": 55,
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
                    "max": 750,
                    "axisLabel": {
                        "show": True,
                        "formatter": "{value}"
                    }
                },
                "yAxis": {
                    "type": "category",
                    "data": product_units["product"].astype(str).tolist(),
                    "axisLabel": {
                        "width": 100,
                        "overflow": "truncate"
                    }
                },
                "series": [{
                    "name": "Units Sold",
                    "type": "bar",
                    "data": [
                        int(value) if float(value).is_integer()
                        else int(value) + 1
                        for value in product_units["quantity"].tolist()
                    ],
                    "barMaxWidth": 24,
                    "itemStyle": {
                        "color": "#4387C5",
                        "borderRadius": [0, 5, 5, 0]
                    },
                    "label": {
                        "show": True,
                        "position": "right",
                        "distance": 6,
                        "color": "#4387C5",
                        "formatter": "{c}"
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
                    "right": 75,
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
                    "max": 65000,
                    "axisLabel": {
                        "show": True,
                        "formatter": "{value}"
                    }
                },
                "yAxis": {
                    "type": "category",
                    "data": product_profit["product"].astype(str).tolist(),
                    "axisLabel": {
                        "width": 100,
                        "overflow": "truncate"
                    }
                },
                "series": [{
                    "name": "Profit ($)",
                    "type": "bar",
                    "data": [
                        int(value) if float(value).is_integer()
                        else int(value) + 1
                        for value in product_profit["profit"].tolist()
                    ],
                    "barMaxWidth": 24,
                    "itemStyle": {
                        "color": "#8E63CE",
                        "borderRadius": [0, 5, 5, 0]
                    },
                    "label": {
                        "show": True,
                        "position": "right",
                        "distance": 6,
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
                "color": [
                    "#4387C5",
                    "#FB8C00",
                    "#8E63CE",
                    "#2E8B57"
                ],
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
                            "name": str(row["sales_channel"]),
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




    







