# imports

import streamlit as st
import pandas as pd
import altair as alt
from streamviz import gauge
import json
import urllib.request
from streamlit_echarts import st_echarts, Map, JsCode
from pathlib import Path

# Load external configuration and front-end assets.
BASE_DIR = Path(__file__).resolve().parent
with (BASE_DIR / "config.json").open(encoding="utf-8") as config_file:
    APP_CONFIG = json.load(config_file)

css_path = BASE_DIR / "style.css"

with (BASE_DIR / "script.js").open(encoding="utf-8") as js_file:
    MAP_TOOLTIP_FORMATTER = JsCode(js_file.read()).js_code

@st.cache_data
def load_world_geojson():
    url = APP_CONFIG["world_geojson_url"]
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.loads(response.read())

# import datasets

df1 = pd.read_csv(BASE_DIR / APP_CONFIG["dataset_path"])

# page config

st.set_page_config("", "", layout="wide")

# Apply custom styles after Streamlit page configuration.
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

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

        st.markdown("""This page provides an overview of the fictional e-commerce dataset used throughout this section. Each subsequent page explores the data from a different perspective, using visualizations to present key business information.""")

        st.divider()

        st.caption("")

        # dataset

        st.subheader("E-commerce Dataset")

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
                    "city",
                    "latitude",
                    "longitude",
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
                    "varchar",
                    "float",
                    "float",
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
                    "Customer's city",
                    "Latitude coordinate of the city",
                    "Longitude coordinate of the city",
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
                with st.popover("Year", use_container_width=True):
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
                with st.popover("Month", use_container_width=True):
                    selected_months = st.multiselect(
                        "Select months",
                        months
                    )

            with quarter_col:
                with st.popover("Quarter", use_container_width=True):
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
                            f"<h3 class='metric-value'>"
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
                                f"<span class='{'delta-positive' if is_favorable else 'delta-negative'}'>"
                                f"{metric['delta']:+.1f}%</span> "
                                f"<span class='delta-label'>"
                                f"{metric['delta_label']}</span>",
                                unsafe_allow_html=True
                            )

                        else:
                            st.markdown(
                                "<span class='delta-placeholder'>&nbsp;</span>",
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
                with st.popover("Category", use_container_width=True):
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
                with st.popover("Channels", use_container_width=True):
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

    
    # Geographical Analysis

    elif page_analysis == 4:

        import unicodedata
        import math

        # Header and filters
        h3, sp17, f3 = st.columns([3, 2, 3])

        with h3:
            st.header("Geographical Business Performance 🌍")

        with f3:
            st.markdown("**Filters**")
            country_col, city_col, category_col2, channel_col2 = st.columns(4)

            # Country filter
            countries = sorted(df1["country"].dropna().unique())

            # Default country: France
            france_index = next(
                (i for i, country in enumerate(countries)
                 if str(country).strip().casefold() == "france"),
                0
            )

            # Initialize the widget state so France is selected on first load
            if countries and st.session_state.get("geo_country_select") not in countries:
                st.session_state["geo_country_select"] = countries[france_index]

            with country_col:
                with st.popover("Country", use_container_width=True):
                    selected_country = st.selectbox(
                        "Select one country",
                        options=countries,
                        index=france_index if countries else None,
                        placeholder="Choose a country",
                        key="geo_country_select"
                    )

            # Cities available in selected country
            selected_country = st.session_state.get("geo_country_select")

            if selected_country:
                city_options = sorted(
                    df1.loc[
                        df1["country"] == selected_country,
                        "city"
                    ].dropna().unique()
                )
            else:
                city_options = []

            # Select all cities by default, and when the country changes
            previous_country = st.session_state.get("geo_previous_country")

            if previous_country != selected_country:
                st.session_state["geo_city_filter"] = city_options.copy()
                st.session_state["geo_previous_country"] = selected_country

            # Remove invalid city selections
            if "geo_city_filter" in st.session_state:
                st.session_state["geo_city_filter"] = [
                    city for city in st.session_state["geo_city_filter"]
                    if city in city_options
                ]

            with city_col:
                with st.popover("City", use_container_width=True):
                    selected_cities = st.multiselect(
                        "Select cities",
                        options=city_options,
                        default=city_options,
                        key="geo_city_filter",
                        disabled=not bool(selected_country)
                    )

            categories = sorted(df1["category"].dropna().unique())
            default_categories = [
                category for category in categories
                if str(category).strip().casefold() in {"books", "electronics"}
            ]
            if "geo_category_filter" not in st.session_state:
                st.session_state["geo_category_filter"] = default_categories

            with category_col2:
                with st.popover("Category", use_container_width=True):
                    selected_categories = st.multiselect(
                        "Select categories",
                        options=categories,
                        default=default_categories,
                        key="geo_category_filter"
                    )

            channels = sorted(df1["sales_channel"].dropna().unique())
            default_channels = [
                channel for channel in channels
                if str(channel).strip().casefold() == "website"
            ]
            if "geo_channel_filter" not in st.session_state:
                st.session_state["geo_channel_filter"] = default_channels

            with channel_col2:
                with st.popover("Channels", use_container_width=True):
                    selected_channels = st.multiselect(
                        "Select channels",
                        options=channels,
                        default=default_channels,
                        key="geo_channel_filter"
                    )

        # Apply filters
        if (
            not selected_country
            or not selected_cities
            or not selected_categories
            or not selected_channels
        ):
            geo_df = df1.iloc[0:0].copy()
        else:
            geo_df = df1[
                (df1["country"] == selected_country)
                & df1["city"].isin(selected_cities)
                & df1["category"].isin(selected_categories)
                & df1["sales_channel"].isin(selected_channels)
            ].copy()

        st.divider()

        # Map and KPI layout
        sp18, map_col, sp19, kpi_col, sp20 = st.columns([0.5, 5, 0.5, 1, 0.5])

        with map_col :
            st.subheader("")
            if not selected_country:
                st.info("Select a country to display the map.")
            elif not selected_cities:
                st.info("Select one or more cities.")
            elif not selected_categories or not selected_channels:
                st.info("Select at least one category and sales channel.")
            elif geo_df.empty:
                st.info("No data available for the selected filters.")
            else:
                city_map = (
                    geo_df.groupby(
                        ["country", "city", "latitude", "longitude"],
                        as_index=False
                    )
                    .agg(
                        revenue=("revenue", "sum"),
                        profit=("profit", "sum"),
                        units_sold=("quantity", "sum"),
                        orders=("order_id", "nunique")
                    )
                    .dropna(subset=["latitude", "longitude"])
                )

                # Limit plotted cities to avoid overloading the map
                MAX_CITIES = 100

                if len(city_map) > MAX_CITIES:
                    city_map = city_map.nlargest(MAX_CITIES, "revenue")

                if city_map.empty:
                    st.info("No valid geographic coordinates available.")
                else:

                    # Normalize country names for GeoJSON matching
                    def normalize_geo_name(value):
                        value = str(value).strip().lower()
                        value = unicodedata.normalize("NFKD", value)
                        return "".join(
                            char for char in value
                            if not unicodedata.combining(char)
                        )

                    # Get country boundaries from GeoJSON
                    def get_country_bounds(geojson, country_name):

                        aliases = {
                            "usa": [
                                "united states",
                                "united states of america"
                            ],
                            "united states": [
                                "united states",
                                "united states of america"
                            ],
                            "united states of america": [
                                "united states",
                                "united states of america"
                            ],
                            "uk": [
                                "uk",
                                "united kingdom",
                                "united kingdom of great britain and northern ireland"
                            ],
                            "united kingdom": [
                                "uk",
                                "united kingdom",
                                "united kingdom of great britain and northern ireland"
                            ],
                            "united kingdom of great britain and northern ireland": [
                                "uk",
                                "united kingdom",
                                "united kingdom of great britain and northern ireland"
                            ],
                        }

                        target = normalize_geo_name(country_name)
                        target_names = aliases.get(target, [target])

                        target_names = [
                            normalize_geo_name(name)
                            for name in target_names
                        ]

                        def collect_coords(obj, result):
                            if isinstance(obj, list):
                                if (
                                    len(obj) >= 2
                                    and isinstance(obj[0], (int, float))
                                    and isinstance(obj[1], (int, float))
                                ):
                                    lon = float(obj[0])
                                    lat = float(obj[1])

                                    if (
                                        math.isfinite(lon)
                                        and math.isfinite(lat)
                                    ):
                                        result.append((lon, lat))
                                else:
                                    for item in obj:
                                        collect_coords(item, result)

                        for feature in geojson.get("features", []):
                            properties = feature.get("properties", {})

                            names = [
                                properties.get("name"),
                                properties.get("NAME"),
                                properties.get("ADMIN"),
                                properties.get("admin"),
                                properties.get("name_en"),
                            ]

                            feature_names = [
                                normalize_geo_name(name)
                                for name in names
                                if name is not None
                            ]

                            if not any(
                                name in target_names
                                for name in feature_names
                            ):
                                continue

                            geometry = feature.get("geometry") or {}
                            coords = []

                            collect_coords(
                                geometry.get("coordinates", []),
                                coords
                            )

                            if not coords:
                                return None

                            longitudes = [point[0] for point in coords]
                            latitudes = [point[1] for point in coords]

                            return {
                                "min_lon": min(longitudes),
                                "max_lon": max(longitudes),
                                "min_lat": min(latitudes),
                                "max_lat": max(latitudes),
                            }

                        return None

                    # Load and register the world map
                    world_geojson = load_world_geojson()

                    world_map = Map(
                        map_name="world",
                        geo_json=world_geojson
                    )

                    # Country-specific boundaries for better framing
                    normalized_country = normalize_geo_name(selected_country)

                    country_bounds_overrides = {
                        # Metropolitan France only, excluding French Guiana
                        "france": {
                            "min_lon": -5.5,
                            "max_lon": 9.8,
                            "min_lat": 41.2,
                            "max_lat": 51.3
                        },

                        # Great Britain and Northern Ireland
                        "united kingdom": {
                            "min_lon": -8.7,
                            "max_lon": 2.0,
                            "min_lat": 49.8,
                            "max_lat": 59.5
                        },
                        "uk": {
                            "min_lon": -8.7,
                            "max_lon": 2.0,
                            "min_lat": 49.8,
                            "max_lat": 59.5
                        },
                        "united kingdom of great britain and northern ireland": {
                            "min_lon": -8.7,
                            "max_lon": 2.0,
                            "min_lat": 49.8,
                            "max_lat": 59.5
                        }
                    }

                    # Use explicit boundaries for France and the UK
                    if normalized_country in country_bounds_overrides:
                        country_bounds = country_bounds_overrides[
                            normalized_country
                        ]
                    else:
                        country_bounds = get_country_bounds(
                            world_geojson,
                            selected_country
                        )

                    geo_options = {
                        "map": "world",
                        "roam": True,
                        "scaleLimit": {
                            "min": 1,
                            "max": 20
                        },
                        "itemStyle": {
                            "areaColor": "#EAF0F6",
                            "borderColor": "#AAB7C4"
                        },
                        "emphasis": {
                            "itemStyle": {
                                "areaColor": "#D2E5F3"
                            }
                        }
                    }

                    # Fit the map to the selected country's boundaries
                    if country_bounds:
                        min_lon = country_bounds["min_lon"]
                        max_lon = country_bounds["max_lon"]
                        min_lat = country_bounds["min_lat"]
                        max_lat = country_bounds["max_lat"]

                        lon_span = max(max_lon - min_lon, 0.1)
                        lat_span = max(max_lat - min_lat, 0.1)

                        # Small padding around the country
                        lon_margin = lon_span * 0.035
                        lat_margin = lat_span * 0.035

                        geo_options["boundingCoords"] = [
                            [
                                min_lon - lon_margin,
                                max_lat + lat_margin
                            ],
                            [
                                max_lon + lon_margin,
                                min_lat - lat_margin
                            ]
                        ]

                    else:
                        # Fallback to coordinates in the dataset
                        country_geo = (
                            df1.loc[
                                df1["country"] == selected_country,
                                ["latitude", "longitude"]
                            ]
                            .copy()
                        )

                        country_geo["latitude"] = pd.to_numeric(
                            country_geo["latitude"],
                            errors="coerce"
                        )
                        country_geo["longitude"] = pd.to_numeric(
                            country_geo["longitude"],
                            errors="coerce"
                        )

                        country_geo = country_geo.replace(
                            [float("inf"), float("-inf")],
                            float("nan")
                        ).dropna()

                        if not country_geo.empty:
                            min_lon = float(country_geo["longitude"].min())
                            max_lon = float(country_geo["longitude"].max())
                            min_lat = float(country_geo["latitude"].min())
                            max_lat = float(country_geo["latitude"].max())

                            lon_span = max(max_lon - min_lon, 0.1)
                            lat_span = max(max_lat - min_lat, 0.1)

                            geo_options["boundingCoords"] = [
                                [
                                    min_lon - lon_span * 0.05,
                                    max_lat + lat_span * 0.05
                                ],
                                [
                                    max_lon + lon_span * 0.05,
                                    min_lat - lat_span * 0.05
                                ]
                            ]

                    # Build native ECharts pie series for each city
                    pie_series = []

                    metric_styles = [
                        {
                            "name": "Revenue",
                            "color": "#2A9D8F",
                            "value_key": "revenue",
                            "format": "currency"
                        },
                        {
                            "name": "Profit",
                            "color": "#E9C46A",
                            "value_key": "profit",
                            "format": "currency"
                        },
                        {
                            "name": "Number of Orders",
                            "color": "#E76F51",
                            "value_key": "orders",
                            "format": "number"
                        },
                        {
                            "name": "Units Sold",
                            "color": "#457B9D",
                            "value_key": "units_sold",
                            "format": "number"
                        }
                    ]

                    # Normalize each metric separately to make all slices visible
                    metric_maxima = {
                        metric["value_key"]: max(
                            float(city_map[metric["value_key"]].max()), 0
                        )
                        for metric in metric_styles
                    }

                    for row in city_map.itertuples():
                        city_name = str(row.city)
                        country_name = str(row.country)

                        pie_data = []

                        for metric in metric_styles:
                            actual_value = float(
                                getattr(row, metric["value_key"])
                            )

                            # Use a common scale for the visual pie slices
                            metric_max = metric_maxima[metric["value_key"]]
                            normalized_value = (
                                max(actual_value, 0) / metric_max * 100
                                if metric_max > 0
                                else 0
                            )

                            pie_data.append({
                                "name": metric["name"],
                                "value": normalized_value,
                                "actualValue": actual_value,
                                "city": city_name,
                                "country": country_name,
                                "format": metric["format"],
                                "itemStyle": {
                                    "color": metric["color"]
                                }
                            })

                        pie_series.append({
                            "name": city_name,
                            "type": "pie",
                            "coordinateSystem": "geo",
                            "center": [
                                float(row.longitude),
                                float(row.latitude)
                            ],
                            "radius": 24,
                            "data": pie_data,
                            "label": {
                                "show": False
                            },
                            "labelLine": {
                                "show": False
                            },
                            "emphasis": {
                                "scale": True,
                                "scaleSize": 5,
                                "itemStyle": {
                                    "shadowBlur": 10,
                                    "shadowColor": "rgba(0, 0, 0, 0.35)"
                                }
                            },
                            "z": 10
                        })

                    map_options = {
                        "tooltip": {
                            "trigger": "item",
                            "formatter": MAP_TOOLTIP_FORMATTER
                        },
                        "geo": geo_options,
                        "series": pie_series
                    }

                    # Recreate the chart when the country changes
                    map_key = (
                        "geographical_sales_map_"
                        + normalize_geo_name(selected_country).replace(" ", "_")
                    )

                    st_echarts(
                        options=map_options,
                        map=world_map,
                        height="550px",
                        key=map_key
                    )

                    # Legend below the map
                    st.markdown(
                        """
                        <div class="map-legend">
                            <div class="legend-item"><span class="legend-dot legend-revenue"></span><span>Revenue</span></div>
                            <div class="legend-item"><span class="legend-dot legend-profit"></span><span>Profit</span></div>
                            <div class="legend-item"><span class="legend-dot legend-orders"></span><span>Number of Orders</span></div>
                            <div class="legend-item"><span class="legend-dot legend-units"></span><span>Units Sold</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Key Performance Indicators
        with kpi_col:
            st.markdown("**Key Metrics**")

            total_revenue = float(geo_df["revenue"].sum())
            total_profit = float(geo_df["profit"].sum())
            total_orders = int(geo_df["order_id"].nunique())
            total_units_sold = int(geo_df["quantity"].sum())

            metric_maxima = {
                "Revenue": max(float(df1["revenue"].sum()), 1),
                "Profit": max(float(df1["profit"].sum()), 1),
                "Number of Orders": max(int(df1["order_id"].nunique()), 1),
                "Units Sold": max(int(df1["quantity"].sum()), 1)
            }

            metric_cards = [
                {
                    "title": "Revenue",
                    "value": f"${total_revenue:,.0f}",
                    "progress": total_revenue / metric_maxima["Revenue"]
                },
                {
                    "title": "Profit",
                    "value": f"${total_profit:,.0f}",
                    "progress": total_profit / metric_maxima["Profit"]
                },
                {
                    "title": "Number of Orders",
                    "value": f"{total_orders:,}",
                    "progress": total_orders / metric_maxima["Number of Orders"]
                },
                {
                    "title": "Units Sold",
                    "value": f"{total_units_sold:,}",
                    "progress": total_units_sold / metric_maxima["Units Sold"]
                }
            ]

            # Colors matching the map legend
            metric_colors = {
                "Revenue": "#2A9D8F",
                "Profit": "#E9C46A",
                "Number of Orders": "#E76F51",
                "Units Sold": "#457B9D"
            }

            for metric in metric_cards:
                with st.container(border=True):
                    st.markdown(f"**{metric['title']}**")
                    st.markdown(
                        f"<h3 class='metric-value'>"
                        f"{metric['value']}</h3>",
                        unsafe_allow_html=True
                    )

                    progress = min(
                        1.0,
                        max(0.0, float(metric["progress"]))
                    )
                    color = metric_colors[metric["title"]]

                    st.markdown(
                        f"""
                        <div class="metric-progress-track">
                            <div class="metric-progress-fill" style="width:{progress * 100:.2f}%; background-color:{color};"></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.caption("")
        st.divider()