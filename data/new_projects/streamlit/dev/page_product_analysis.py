# product sales analysis page

import pandas as pd
import streamlit as st

from shared import render_echarts_chart

def render_product_analysis_page(df1: pd.DataFrame) -> None:

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

                render_echarts_chart(
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

                render_echarts_chart(
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

                render_echarts_chart(
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

                render_echarts_chart(
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

                render_echarts_chart(
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

                render_echarts_chart(
                    channel_options,
                    height=300,
                    key="channel_revenue_echart"
                )

            # create the dashboard footer section

            st.subheader("")
            st.divider()
