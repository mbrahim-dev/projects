# imports

import streamlit as st
import pandas as pd
import altair as alt
from streamviz import gauge
import json
import urllib.request
from streamlit_echarts import st_echarts, Map, JsCode

@st.cache_data
def load_world_geojson():
    url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.loads(response.read())

# import datasets

df1 = pd.read_csv("data/new_projects/streamlit/dataset/sales_performance.csv")

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

        h1, sp6, f1 = st.columns([3, 2, 3])

        with h1:
            st.header("Business Performance Over Time 📊")
            st.caption("")

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
                    default=[2025] if 2025 in available_years else available_years[:1]
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
        st.caption("")

        if selected_years:

            # get the comparison year automatically

            selected_year = int(selected_years[0]) if len(selected_years) == 1 else None
            comparison_year = selected_year - 1 if selected_year is not None else None
            has_comparison_year = (
                comparison_year is not None
                and comparison_year in available_years
            )

            # apply filters

            chart_data = df1[df1["year"].isin(selected_years)].copy()

            if selected_months:
                chart_data = chart_data[chart_data["month_name"].isin(selected_months)]

            if selected_quarters:
                chart_data = chart_data[chart_data["quarter"].isin(selected_quarters)]

            # calculate key metrics

            revenue = float(chart_data["revenue"].sum())
            profit = float(chart_data["profit"].sum())
            number_of_orders = int(chart_data["order_id"].nunique())
            total_costs = float(chart_data["cost"].sum())

            # calculate year-over-year variations for a single selected year

            revenue_delta = None
            profit_delta = None
            orders_delta = None
            costs_delta = None

            if has_comparison_year:

                comparison_data = df1[df1["year"] == comparison_year].copy()

                if selected_months:
                    comparison_data = comparison_data[comparison_data["month_name"].isin(selected_months)]

                if selected_quarters:
                    comparison_data = comparison_data[comparison_data["quarter"].isin(selected_quarters)]

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

            # calculate reference values for the metric progress bars

            metric_maxima = {
                "Revenue": max(float(df1["revenue"].sum()), 1),
                "Profit": max(float(df1["profit"].sum()), 1),
                "Number of Orders": max(int(df1["order_id"].nunique()), 1),
                "Total Costs": max(float(df1["cost"].sum()), 1)
            }

            # prepare key metric cards

            metric_cards = [
                {
                    "title": "Revenue",
                    "value": f"${revenue:,.0f}",
                    "delta": revenue_delta,
                    "delta_label": f"vs {comparison_year}" if has_comparison_year else "",
                    "progress": min(1.0, max(0.0, revenue / metric_maxima["Revenue"]))
                },
                {
                    "title": "Profit",
                    "value": f"${profit:,.0f}",
                    "delta": profit_delta,
                    "delta_label": f"vs {comparison_year}" if has_comparison_year else "",
                    "progress": min(1.0, max(0.0, profit / metric_maxima["Profit"]))
                },
                {
                    "title": "Number of Orders",
                    "value": f"{number_of_orders:,}",
                    "delta": orders_delta,
                    "delta_label": f"vs {comparison_year}" if has_comparison_year else "",
                    "progress": min(1.0, max(0.0, number_of_orders / metric_maxima["Number of Orders"]))
                },
                {
                    "title": "Total Costs",
                    "value": f"${total_costs:,.0f}",
                    "delta": costs_delta,
                    "delta_label": f"vs {comparison_year}" if has_comparison_year else "",
                    "progress": min(1.0, max(0.0, total_costs / metric_maxima["Total Costs"]))
                }
            ]

            # display four key metrics horizontally

            st.markdown("**Key Metrics**")
            st.caption("")

            kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")

            for column, metric in zip([kpi1, kpi2, kpi3, kpi4],metric_cards):
                
                with column:
                    with st.container(border=True):

                        st.markdown(f"**{metric['title']}**")

                        st.markdown(
                            f"<h3 style='margin:0;color:#000000'>"
                            f"{metric['value']}</h3>",
                            unsafe_allow_html=True
                        )

                        if metric["delta"] is not None:

                            is_favorable = (
                                metric["delta"] <= 0
                                if metric["title"] == "Total Costs"
                                else metric["delta"] >= 0
                            )

                            delta_color = (
                                "#2E8B57" if is_favorable else "#E53935"
                            )

                            st.markdown(
                                f"<span style='color:{delta_color};font-size:12px'>"
                                f"{metric['delta']:+.1f}%</span> "
                                f"<span style='font-size:12px;color:#666666'>"
                                f"{metric['delta_label']}</span>",
                                unsafe_allow_html=True
                            )

                        else:
                            st.markdown(
                                "<span style='font-size:12px'>&nbsp;</span>",
                                unsafe_allow_html=True
                            )

                        st.progress(
                            min(
                                1.0,
                                max(0.0, float(metric["progress"]))
                            )
                        )

            # add spacing between metrics and charts

            st.subheader("")

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

            # prepare monthly revenue series

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

            # prepare monthly profit series

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

            # prepare quarterly revenue series

            quarter_labels = ["Q1", "Q2", "Q3", "Q4"]
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

            # configure monthly revenue chart

            revenue_options = {
                "animation": True,
                "grid": {
                    "left": 55,
                    "right": 20,
                    "top": 45,
                    "bottom": 65,
                    "containLabel": True
                },
                "tooltip": {
                    "trigger": "axis",
                    "confine": True,
                    "axisPointer": {"type": "line"}
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

            # configure monthly profit chart

            profit_options = {
                "animation": True,
                "grid": {
                    "left": 55,
                    "right": 20,
                    "top": 45,
                    "bottom": 65,
                    "containLabel": True
                },
                "tooltip": {
                    "trigger": "axis",
                    "confine": True,
                    "axisPointer": {"type": "line"}
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

            # configure quarterly revenue chart

            quarter_options = {
                "animation": True,
                "grid": {
                    "left": 55,
                    "right": 20,
                    "top": 45,
                    "bottom": 45,
                    "containLabel": True
                },
                "tooltip": {
                    "trigger": "axis",
                    "confine": True,
                    "axisPointer": {"type": "shadow"}
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

            # display the three charts horizontally

            c1, sp9, c2, sp10, c3 = st.columns([1, 0.3, 1, 0.3, 1])

            with c1:
                st.markdown("**Monthly Revenue Comparison**")
                st.caption("")

                st.echarts_chart(
                    revenue_options,
                    height=320,
                    key="monthly_revenue_echart"
                )

            with c2:
                st.markdown("**Monthly Profit Comparison**")
                st.caption("")


                st.echarts_chart(
                    profit_options,
                    height=320,
                    key="monthly_profit_echart"
                )

            with c3:
                st.markdown("**Quarterly Revenue Comparison**")
                st.caption("")

                st.echarts_chart(
                    quarter_options,
                    height=320,
                    key="quarterly_revenue_echart"
                )

            # add spacing below the charts
            
            st.divider()

        else:
            st.info("Please select at least one year to display the analysis.")


##########################################################################################

    # product analysis
    
    elif page_analysis == 3:
    
        # create the header and filter columns
    
        h2, sp11, f2 = st.columns([3, 2, 3])
    
        with h2:
            st.header("Product Sales Analysis 🛍️")
            st.caption("")
    
        with f2:
            st.markdown("**Filters**")
    
            category_col, channel_col = st.columns(2)
    
            with category_col:
                with st.popover("Category"):
                    available_categories = sorted(
                        df1["category"].dropna().unique().tolist()
                    )
    
                    selected_category = st.selectbox(
                        "Select a category",
                        options=["All"] + available_categories,
                        index=(available_categories.index("Books") + 1)
                        if "Books" in available_categories else 0
                    )
    
            with channel_col:
                with st.popover("Channels"):
                    available_channels = sorted(
                        df1["sales_channel"].dropna().unique().tolist()
                    )
    
                    default_channels = [
                        channel for channel in ["Marketplace", "Mobile App"]
                        if channel in available_channels
                    ]
    
                    selected_channels = st.multiselect(
                        "Select channels",
                        options=available_channels,
                        default=default_channels
                    )
    
        st.subheader("")
        st.divider()

        # filter the dataset

        filtered_df = df1.copy()

        if selected_category != "All":
            filtered_df = filtered_df[
                filtered_df["category"] == selected_category
            ]

        if selected_channels:
            filtered_df = filtered_df[
                filtered_df["sales_channel"].isin(selected_channels)
            ]
        else:
            filtered_df = filtered_df.iloc[0:0]

        # define a coordinated color palette

        color_units = "#356B8C"
        color_revenue = "#2A9D8F"
        color_profit = "#E76F51"
        color_channels = ["#356B8C", "#2A9D8F", "#E76F51", "#E9C46A"]

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

        # set gauge ranges and fill them for the complete dataset

        show_all_data = (
            selected_category == "All"
            and set(selected_channels) == set(available_channels)
        )

        max_units = max(units_sold, 1) if show_all_data else 30000
        max_revenue = max(total_revenue, 1) if show_all_data else 5000000
        max_profit = max(total_profit, 1) if show_all_data else 2000000

        # create the three gauges

        g1, sp13, g2, sp14, g3 = st.columns([1, 0.3, 1, 0.3, 1])

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
                        "itemStyle": {"color": color_units}
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
                        "color": color_units,
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

        # display the profit circular gauge

        with g2:

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
                        "itemStyle": {"color": color_profit}
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
                        "color": color_profit,
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

        # display the revenue circular gauge

        with g3:

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
                        "itemStyle": {"color": color_revenue}
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
                        "color": color_revenue,
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
            filtered_df.groupby("sales_channel", as_index=False)
            .agg(Revenue=("revenue", "sum"))
            .sort_values("Revenue", ascending=False)
        )

        st.subheader("")

        # create the chart columns

        c1, sp15, c2, sp16, c3 = st.columns([1, 0.3, 1, 0.3, 1])

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
                        "color": color_units,
                        "borderRadius": [0, 5, 5, 0]
                    },
                    "label": {
                        "show": True,
                        "position": "right",
                        "distance": 6,
                        "color": color_units,
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
                        "color": color_profit,
                        "borderRadius": [0, 5, 5, 0]
                    },
                    "label": {
                        "show": True,
                        "position": "right",
                        "distance": 6,
                        "color": color_profit,
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
                "color": color_channels,
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
        

##########################################################################################


    
    # geographic analysis

    elif page_analysis == 4:

        import math
        import unicodedata
    
        st.markdown("## Geographical Sales Analysis")
    
        def normalize_geo_name(value):
            value = str(value).strip().lower()
            value = unicodedata.normalize("NFKD", value)
            value = "".join(
                char for char in value
                if not unicodedata.combining(char)
            )
            return value.replace("&", "and").strip()
    
        def extract_geo_coordinates(coordinates, result=None):
            if result is None:
                result = []
    
            if (
                isinstance(coordinates, (list, tuple))
                and len(coordinates) >= 2
                and isinstance(coordinates[0], (int, float))
                and isinstance(coordinates[1], (int, float))
            ):
                result.append((coordinates[0], coordinates[1]))
            elif isinstance(coordinates, (list, tuple)):
                for item in coordinates:
                    extract_geo_coordinates(item, result)
    
            return result
    
        def get_country_bounds(feature):
            geometry = feature.get("geometry", {})
            coordinates = geometry.get("coordinates", [])
            points = extract_geo_coordinates(coordinates)
    
            if not points:
                return None
    
            longitudes = [point[0] for point in points]
            latitudes = [point[1] for point in points]
    
            return {
                "min_lon": min(longitudes),
                "max_lon": max(longitudes),
                "min_lat": min(latitudes),
                "max_lat": max(latitudes),
            }
    
        required_columns = [
            "order_id",
            "country",
            "city",
            "category",
            "sales_channel",
            "latitude",
            "longitude",
            "revenue",
            "profit",
            "quantity",
        ]
    
        missing_columns = [
            column for column in required_columns
            if column not in df1.columns
        ]
    
        if missing_columns:
            st.error(
                "The dataset is missing the following required columns: "
                + ", ".join(missing_columns)
            )
    
        else:
    
            geo_df_all = df1.copy()
    
            for column in [
                "latitude",
                "longitude",
                "revenue",
                "profit",
                "quantity",
            ]:
                geo_df_all[column] = pd.to_numeric(
                    geo_df_all[column],
                    errors="coerce"
                )
    
            geo_df_all["country"] = (
                geo_df_all["country"].fillna("").astype(str).str.strip()
            )
            geo_df_all["city"] = (
                geo_df_all["city"].fillna("").astype(str).str.strip()
            )
            geo_df_all["category"] = (
                geo_df_all["category"].fillna("").astype(str).str.strip()
            )
            geo_df_all["sales_channel"] = (
                geo_df_all["sales_channel"].fillna("").astype(str).str.strip()
            )
    
            geo_df_all = geo_df_all[
                (geo_df_all["country"] != "")
                & geo_df_all["latitude"].notna()
                & geo_df_all["longitude"].notna()
            ].copy()
    
            if geo_df_all.empty:
                st.warning(
                    "No valid geographical data is available in the dataset."
                )
    
            else:
    
                filter_col1, filter_col2, filter_col3, filter_col4 = (
                    st.columns(4)
                )
    
                countries = sorted(
                    geo_df_all["country"].unique().tolist()
                )
    
                with filter_col1:
                    with st.popover("Country", use_container_width=True):
                        selected_country = st.selectbox(
                            "Select a country",
                            options=countries,
                            index=None,
                            placeholder="Choose a country",
                            key="geo_country_filter",
                        )
    
                if selected_country:
                    country_df = geo_df_all[
                        geo_df_all["country"] == selected_country
                    ].copy()
                else:
                    country_df = geo_df_all.iloc[0:0].copy()
    
                city_options = sorted(
                    country_df.loc[
                        country_df["city"] != "", "city"
                    ].unique().tolist()
                )
    
                with filter_col2:
                    with st.popover("City", use_container_width=True):
                        selected_cities = st.multiselect(
                            "Select one or more cities",
                            options=city_options,
                            default=[],
                            key=(
                                "geo_city_filter_"
                                + normalize_geo_name(selected_country or "none")
                            ),
                        )
    
                categories = sorted(
                    geo_df_all.loc[
                        geo_df_all["category"] != "", "category"
                    ].unique().tolist()
                )
    
                with filter_col3:
                    with st.popover("Category", use_container_width=True):
                        selected_categories = st.multiselect(
                            "Select categories",
                            options=categories,
                            default=[],
                            key="geo_category_filter",
                        )
    
                channels = sorted(
                    geo_df_all.loc[
                        geo_df_all["sales_channel"] != "",
                        "sales_channel",
                    ].unique().tolist()
                )
    
                with filter_col4:
                    with st.popover("Sales Channel", use_container_width=True):
                        selected_channels = st.multiselect(
                            "Select sales channels",
                            options=channels,
                            default=[],
                            key="geo_channel_filter",
                        )
    
                filters_complete = (
                    selected_country is not None
                    and len(selected_cities) > 0
                    and len(selected_categories) > 0
                    and len(selected_channels) > 0
                )
    
                if not filters_complete:
                    st.info(
                        "Select a country, at least one city, "
                        "a category and a sales channel to display the map."
                    )
    
                else:
    
                    geo_df = geo_df_all[
                        (geo_df_all["country"] == selected_country)
                        & (geo_df_all["city"].isin(selected_cities))
                        & (geo_df_all["category"].isin(selected_categories))
                        & (geo_df_all["sales_channel"].isin(selected_channels))
                    ].copy()
    
                    if geo_df.empty:
                        st.warning(
                            "No sales data matches the selected filters."
                        )
    
                    else:
    
                        city_map = (
                            geo_df.groupby(
                                [
                                    "country",
                                    "city",
                                    "latitude",
                                    "longitude",
                                ],
                                as_index=False,
                            )
                            .agg(
                                revenue=("revenue", "sum"),
                                profit=("profit", "sum"),
                                units_sold=("quantity", "sum"),
                                orders=("order_id", "nunique"),
                            )
                        )
    
                        city_map = city_map.dropna(
                            subset=["latitude", "longitude"]
                        ).copy()
    
                        city_map = city_map.head(100)

                        city_map["pie_revenue"] = (
                            city_map["revenue"].clip(lower=0)
                        )
                        city_map["pie_profit"] = (
                            city_map["profit"].clip(lower=0)
                        )
                        city_map["pie_orders"] = (
                            city_map["orders"].clip(lower=0)
                        )
                        city_map["pie_units"] = (
                            city_map["units_sold"].clip(lower=0)
                        )
    
                        pie_data = []
    
                        for row in city_map.itertuples():
                            pie_data.append(
                                {
                                    "name": str(row.city),
                                    "country": str(row.country),
                                    "value": [
                                        float(row.longitude),
                                        float(row.latitude),
                                        float(row.pie_revenue),
                                        float(row.pie_profit),
                                        float(row.pie_orders),
                                        float(row.pie_units),
                                    ],
                                    "revenue": float(row.revenue),
                                    "profit": float(row.profit),
                                    "orders": int(row.orders),
                                    "units_sold": float(row.units_sold),
                                }
                            )
    
                        total_revenue = float(geo_df["revenue"].sum())
                        total_profit = float(geo_df["profit"].sum())
                        total_orders = int(geo_df["order_id"].nunique())
                        total_units = float(geo_df["quantity"].sum())
    
                        all_revenue = float(
                            pd.to_numeric(
                                df1["revenue"], errors="coerce"
                            ).sum()
                        )
                        all_profit = float(
                            pd.to_numeric(
                                df1["profit"], errors="coerce"
                            ).sum()
                        )
                        all_orders = int(df1["order_id"].nunique())
                        all_units = float(
                            pd.to_numeric(
                                df1["quantity"], errors="coerce"
                            ).sum()
                        )
    
                        def safe_progress(value, total):
                            if total <= 0:
                                return 0.0
                            return min(max(value / total, 0.0), 1.0)
    
                        map_col, kpi_col = st.columns(
                            [3.4, 1],
                            gap="large",
                        )
    
                        with map_col:
        
                            world_geojson = load_world_geojson()
    
                            country_aliases = {
                                "usa": "united states of america",
                                "united states": "united states of america",
                                "uk": "united kingdom",
                                "south korea": "south korea",
                                "russia": "russia",
                                "ivory coast": "cote d'ivoire",
                            }
    
                            selected_country_normalized = normalize_geo_name(
                                selected_country
                            )
    
                            target_country_name = country_aliases.get(
                                selected_country_normalized,
                                selected_country_normalized,
                            )
    
                            country_feature = None
    
                            for feature in world_geojson.get("features", []):
                                properties = feature.get("properties", {})
    
                                geo_names = [
                                    properties.get("name", ""),
                                    properties.get("NAME", ""),
                                    properties.get("ADMIN", ""),
                                    properties.get("name_long", ""),
                                ]
    
                                normalized_names = [
                                    normalize_geo_name(name)
                                    for name in geo_names
                                    if name
                                ]
    
                                normalized_names = [
                                    country_aliases.get(name, name)
                                    for name in normalized_names
                                ]
    
                                if target_country_name in normalized_names:
                                    country_feature = feature
                                    break
    
                            country_bounds_overrides = {
                                "france": {
                                    "min_lon": -5.5,
                                    "max_lon": 9.8,
                                    "min_lat": 41.2,
                                    "max_lat": 51.3,
                                },
                                "united kingdom": {
                                    "min_lon": -8.7,
                                    "max_lon": 2.0,
                                    "min_lat": 49.8,
                                    "max_lat": 59.5,
                                },
                                "uk": {
                                    "min_lon": -8.7,
                                    "max_lon": 2.0,
                                    "min_lat": 49.8,
                                    "max_lat": 59.5,
                                },
                                "united kingdom of great britain and northern ireland": {
                                    "min_lon": -8.7,
                                    "max_lon": 2.0,
                                    "min_lat": 49.8,
                                    "max_lat": 59.5,
                                },
                            }
    
                            country_bounds = country_bounds_overrides.get(
                                selected_country_normalized
                            )
    
                            if country_bounds is None and country_feature:
                                country_bounds = get_country_bounds(
                                    country_feature
                                )
    
                            if country_bounds is None:
                                country_bounds = {
                                    "min_lon": float(city_map["longitude"].min()),
                                    "max_lon": float(city_map["longitude"].max()),
                                    "min_lat": float(city_map["latitude"].min()),
                                    "max_lat": float(city_map["latitude"].max()),
                                }
    
                            lon_span = max(
                                country_bounds["max_lon"]
                                - country_bounds["min_lon"],
                                0.5,
                            )
                            lat_span = max(
                                country_bounds["max_lat"]
                                - country_bounds["min_lat"],
                                0.5,
                            )
    
                            lon_padding = lon_span * 0.06
                            lat_padding = lat_span * 0.06
    
                            bounding_coords = [
                                [
                                    country_bounds["min_lon"] - lon_padding,
                                    country_bounds["max_lat"] + lat_padding,
                                ],
                                [
                                    country_bounds["max_lon"] + lon_padding,
                                    country_bounds["min_lat"] - lat_padding,
                                ],
                            ]
    
                            map_options = {
                                "backgroundColor": "transparent",
                                "animation": True,
                                "tooltip": {
                                    "trigger": "item",
                                    "confine": True,
                                    "backgroundColor": "rgba(30, 30, 30, 0.95)",
                                    "borderWidth": 0,
                                    "textStyle": {
                                        "color": "#FFFFFF",
                                        "fontSize": 12,
                                    },
                                    "formatter": """
                                        function(params) {
                                            var d = params.data;
    
                                            if (!d) {
                                                return '';
                                            }
    
                                            var values = d.value || [];
                                            var revenue = Math.max(0, Number(values[2]) || 0);
                                            var profit = Math.max(0, Number(values[3]) || 0);
                                            var orders = Math.max(0, Number(values[4]) || 0);
                                            var units = Math.max(0, Number(values[5]) || 0);
                                            var total = revenue + profit + orders + units;
    
                                            function fmt(v) {
                                                return Number(v).toLocaleString(
                                                    undefined,
                                                    { maximumFractionDigits: 2 }
                                                );
                                            }
    
                                            function pct(v) {
                                                return total > 0
                                                    ? (v / total * 100).toFixed(1) + '%'
                                                    : '0.0%';
                                            }
    
                                            return '<b>' + d.name + '</b><br/>' +
                                                '<span style="color:#2A9D8F">●</span> Revenue: ' +
                                                fmt(d.revenue) + ' (' + pct(revenue) + ')<br/>' +
                                                '<span style="color:#E9C46A">●</span> Profit: ' +
                                                fmt(d.profit) + ' (' + pct(profit) + ')<br/>' +
                                                '<span style="color:#E76F51">●</span> Number of Orders: ' +
                                                fmt(d.orders) + ' (' + pct(orders) + ')<br/>' +
                                                '<span style="color:#457B9D">●</span> Units Sold: ' +
                                                fmt(d.units_sold) + ' (' + pct(units) + ')';
                                        }
                                    """,
                                },
                                "geo": {
                                    "map": "world",
                                    "roam": True,
                                    "boundingCoords": bounding_coords,
                                    "layoutCenter": ["50%", "50%"],
                                    "layoutSize": "100%",
                                    "itemStyle": {
                                        "areaColor": "#E8EDF2",
                                        "borderColor": "#FFFFFF",
                                        "borderWidth": 0.7,
                                    },
                                    "emphasis": {
                                        "itemStyle": {
                                            "areaColor": "#D5DEE8",
                                        }
                                    },
                                },
                                "series": [
                                    {
                                        "name": "City Sales",
                                        "type": "custom",
                                        "coordinateSystem": "geo",
                                        "renderItem": """
                                            function(params, api) {
                                                var lon = api.value(0);
                                                var lat = api.value(1);
    
                                                var revenue = Math.max(0, Number(api.value(2)) || 0);
                                                var profit = Math.max(0, Number(api.value(3)) || 0);
                                                var orders = Math.max(0, Number(api.value(4)) || 0);
                                                var units = Math.max(0, Number(api.value(5)) || 0);
    
                                                var values = [revenue, profit, orders, units];
                                                var colors = [
                                                    '#2A9D8F',
                                                    '#E9C46A',
                                                    '#E76F51',
                                                    '#457B9D'
                                                ];
    
                                                var total = values.reduce(
                                                    function(sum, value) {
                                                        return sum + value;
                                                    },
                                                    0
                                                );
    
                                                var point = api.coord([lon, lat]);
    
                                                if (
                                                    !point ||
                                                    !isFinite(point[0]) ||
                                                    !isFinite(point[1])
                                                ) {
                                                    return null;
                                                }
    
                                                if (total <= 0) {
                                                    return {
                                                        type: 'circle',
                                                        shape: {
                                                            cx: point[0],
                                                            cy: point[1],
                                                            r: 4
                                                        },
                                                        style: {
                                                            fill: '#777777',
                                                            stroke: '#FFFFFF',
                                                            lineWidth: 1
                                                        }
                                                    };
                                                }
    
                                                var radius = 28;
                                                var startAngle = -Math.PI / 2;
                                                var children = [];
    
                                                for (var i = 0; i < values.length; i++) {
                                                    if (values[i] <= 0) {
                                                        continue;
                                                    }
    
                                                    var endAngle = startAngle +
                                                        (values[i] / total) * Math.PI * 2;
    
                                                    children.push({
                                                        type: 'sector',
                                                        shape: {
                                                            cx: point[0],
                                                            cy: point[1],
                                                            r: radius,
                                                            r0: 0,
                                                            startAngle: startAngle,
                                                            endAngle: endAngle,
                                                            clockwise: true
                                                        },
                                                        style: {
                                                            fill: colors[i],
                                                            stroke: '#FFFFFF',
                                                            lineWidth: 1.5,
                                                            opacity: 0.95
                                                        },
                                                        emphasis: {
                                                            style: {
                                                                opacity: 1,
                                                                lineWidth: 3,
                                                                shadowBlur: 12,
                                                                shadowColor: colors[i]
                                                            }
                                                        },
                                                        z2: 10
                                                    });
    
                                                    startAngle = endAngle;
                                                }
    
                                                return {
                                                    type: 'group',
                                                    children: children,
                                                    emphasis: {
                                                        focus: 'self'
                                                    },
                                                    z2: 10
                                                };
                                            }
                                        """,
                                        "dimensions": [
                                            "longitude",
                                            "latitude",
                                            "revenue",
                                            "profit",
                                            "orders",
                                            "units_sold",
                                        ],
                                        "encode": {
                                            "tooltip": [
                                                "revenue",
                                                "profit",
                                                "orders",
                                                "units_sold",
                                            ],
                                        },
                                        "data": pie_data,
                                        "silent": False,
                                        "z": 10,
                                    }
                                ],
                            }
    
                            world_map = Map(
                                map_name="world",
                                geo_json=world_geojson,
                            )
    
                            map_key = (
                                "geographical_sales_map_"
                                + normalize_geo_name(selected_country).replace(
                                    " ", "_"
                                )
                            )
    
                            st_echarts(
                                options=map_options,
                                map=world_map,
                                height="550px",
                                key=map_key,
                            )
    
                            st.markdown(
                                """
                                <div style="
                                    display:flex;
                                    justify-content:center;
                                    align-items:center;
                                    flex-wrap:wrap;
                                    gap:22px;
                                    margin-top:12px;
                                    padding:10px 0;
                                ">
                                    <div style="display:flex;align-items:center;gap:7px;">
                                        <span style="
                                            width:13px;height:13px;border-radius:50%;
                                            background:#2A9D8F;display:inline-block;
                                        "></span>
                                        <span>Revenue</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:7px;">
                                        <span style="
                                            width:13px;height:13px;border-radius:50%;
                                            background:#E9C46A;display:inline-block;
                                        "></span>
                                        <span>Profit</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:7px;">
                                        <span style="
                                            width:13px;height:13px;border-radius:50%;
                                            background:#E76F51;display:inline-block;
                                        "></span>
                                        <span>Number of Orders</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:7px;">
                                        <span style="
                                            width:13px;height:13px;border-radius:50%;
                                            background:#457B9D;display:inline-block;
                                        "></span>
                                        <span>Units Sold</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
    
                        with kpi_col:
    
                            st.markdown("### Key Metrics")
    
                            st.markdown(
                                f"""
                                <div style="
                                    border:1px solid rgba(128,128,128,0.25);
                                    border-radius:12px;
                                    padding:14px;
                                    margin-bottom:12px;
                                ">
                                    <div style="font-size:13px;opacity:0.75;">
                                        Revenue
                                    </div>
                                    <div style="font-size:25px;font-weight:700;">
                                        {total_revenue:,.2f}
                                    </div>
                                    <div style="
                                        background:rgba(128,128,128,0.18);
                                        border-radius:5px;height:6px;margin-top:10px;
                                    ">
                                        <div style="
                                            background:#2A9D8F;
                                            width:{safe_progress(total_revenue, all_revenue) * 100:.1f}%;
                                            height:6px;border-radius:5px;
                                        "></div>
                                    </div>
                                    <div style="font-size:11px;opacity:0.65;margin-top:5px;">
                                        Share of overall revenue
                                    </div>
                                </div>
    
                                <div style="
                                    border:1px solid rgba(128,128,128,0.25);
                                    border-radius:12px;
                                    padding:14px;
                                    margin-bottom:12px;
                                ">
                                    <div style="font-size:13px;opacity:0.75;">
                                        Profit
                                    </div>
                                    <div style="font-size:25px;font-weight:700;">
                                        {total_profit:,.2f}
                                    </div>
                                    <div style="
                                        background:rgba(128,128,128,0.18);
                                        border-radius:5px;height:6px;margin-top:10px;
                                    ">
                                        <div style="
                                            background:#E9C46A;
                                            width:{safe_progress(max(total_profit, 0), max(all_profit, 0)) * 100:.1f}%;
                                            height:6px;border-radius:5px;
                                        "></div>
                                    </div>
                                    <div style="font-size:11px;opacity:0.65;margin-top:5px;">
                                        Share of overall positive profit
                                    </div>
                                </div>
    
                                <div style="
                                    border:1px solid rgba(128,128,128,0.25);
                                    border-radius:12px;
                                    padding:14px;
                                    margin-bottom:12px;
                                ">
                                    <div style="font-size:13px;opacity:0.75;">
                                        Number of Orders
                                    </div>
                                    <div style="font-size:25px;font-weight:700;">
                                        {total_orders:,}
                                    </div>
                                    <div style="
                                        background:rgba(128,128,128,0.18);
                                        border-radius:5px;height:6px;margin-top:10px;
                                    ">
                                        <div style="
                                            background:#E76F51;
                                            width:{safe_progress(total_orders, all_orders) * 100:.1f}%;
                                            height:6px;border-radius:5px;
                                        "></div>
                                    </div>
                                    <div style="font-size:11px;opacity:0.65;margin-top:5px;">
                                        Share of overall orders
                                    </div>
                                </div>
    
                                <div style="
                                    border:1px solid rgba(128,128,128,0.25);
                                    border-radius:12px;
                                    padding:14px;
                                    margin-bottom:12px;
                                ">
                                    <div style="font-size:13px;opacity:0.75;">
                                        Units Sold
                                    </div>
                                    <div style="font-size:25px;font-weight:700;">
                                        {total_units:,.0f}
                                    </div>
                                    <div style="
                                        background:rgba(128,128,128,0.18);
                                        border-radius:5px;height:6px;margin-top:10px;
                                    ">
                                        <div style="
                                            background:#457B9D;
                                            width:{safe_progress(total_units, all_units) * 100:.1f}%;
                                            height:6px;border-radius:5px;
                                        "></div>
                                    </div>
                                    <div style="font-size:11px;opacity:0.65;margin-top:5px;">
                                        Share of overall units sold
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

        # Footer
        st.subheader("")
        st.divider()






