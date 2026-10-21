# time-based sales analysis page

import pandas as pd
import streamlit as st

from shared import (render_echarts_chart, render_metric_delta, render_metric_delta_empty, render_metric_value)

def render_time_analysis_page(df1: pd.DataFrame) -> None:

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

                            render_metric_value(metric["value"])

                            if metric["delta"] is not None:

                                is_favorable = (
                                    metric["delta"] <= 0
                                    if metric["title"] == "Total Costs"
                                    else metric["delta"] >= 0
                                )

                                delta_color = (
                                    "#2E8B57" if is_favorable else "#E53935"
                                )

                                render_metric_delta(color=delta_color, delta=f"{metric['delta']:+.1f}%", label=metric["delta_label"])

                            else:
                                render_metric_delta_empty()

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

                    render_echarts_chart(
                        revenue_options,
                        height=320,
                        key="monthly_revenue_echart"
                    )

                with c2:
                    st.markdown("**Monthly Profit Comparison**")
                    st.caption("")

                    render_echarts_chart(
                        profit_options,
                        height=320,
                        key="monthly_profit_echart"
                    )

                with c3:
                    st.markdown("**Quarterly Revenue Comparison**")
                    st.caption("")

                    render_echarts_chart(
                        quarter_options,
                        height=320,
                        key="quarterly_revenue_echart"
                    )

                # add spacing below the charts

                st.divider()

            else:
                st.info("Please select at least one year to display the analysis.")
