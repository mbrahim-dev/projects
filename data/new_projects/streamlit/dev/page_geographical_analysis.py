# geographical sales analysis page

import json
import urllib.request

import pandas as pd
import streamlit as st

from streamlit_echarts import Map, JsCode

from shared import render_streamlit_echarts, render_metric_value, render_progress_bar, load_text_asset, render_html_template

@st.cache_data
def load_world_geojson():

    # load the geojson used to draw the world map

    url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.loads(response.read())

def render_geographical_analysis_page(df1: pd.DataFrame) -> None:
    import unicodedata
    import math

    # header and filters

    h3, sp17, f3 = st.columns([3, 2, 3])

    with h3:
        st.header("Geographical Business Performance 🌍")

    with f3:
        st.markdown("**Filters**")
        country_col, city_col, category_col2, channel_col2 = st.columns(4)

        # country filter

        countries = sorted(df1["country"].dropna().unique())

        # default country: france

        france_index = next(
            (i for i, country in enumerate(countries)
             if str(country).strip().casefold() == "france"),
            0
        )

        # initialize the widget state so france is selected on first load

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

        # cities available in selected country

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

        # select all cities by default, and when the country changes

        previous_country = st.session_state.get("geo_previous_country")

        if previous_country != selected_country:
            st.session_state["geo_city_filter"] = city_options.copy()
            st.session_state["geo_previous_country"] = selected_country

        # remove invalid city selections

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

    # apply filters

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

    # map and kpi layout

    map_col, sp18, kpi_col, sp19 = st.columns([6, 0.5, 1, 0.5])

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

            # limit plotted cities to avoid overloading the map

            MAX_CITIES = 100

            if len(city_map) > MAX_CITIES:
                city_map = city_map.nlargest(MAX_CITIES, "revenue")

            if city_map.empty:
                st.info("No valid geographic coordinates available.")
            else:

                # normalize country names for geojson matching

                def normalize_geo_name(value):
                    value = str(value).strip().lower()
                    value = unicodedata.normalize("NFKD", value)
                    return "".join(
                        char for char in value
                        if not unicodedata.combining(char)
                    )

                # get country boundaries from geojson

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

                # load and register the world map

                world_geojson = load_world_geojson()

                world_map = Map(
                    map_name="world",
                    geo_json=world_geojson
                )

                # country-specific boundaries for better framing

                normalized_country = normalize_geo_name(selected_country)

                country_bounds_overrides = {

                    # metropolitan france only, excluding french guiana

                    "france": {
                        "min_lon": -5.5,
                        "max_lon": 9.8,
                        "min_lat": 41.2,
                        "max_lat": 51.3
                    },

                    # great britain and northern ireland

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

                # use explicit boundaries for france and the uk

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

                # fit the map to the selected country's boundaries

                if country_bounds:
                    min_lon = country_bounds["min_lon"]
                    max_lon = country_bounds["max_lon"]
                    min_lat = country_bounds["min_lat"]
                    max_lat = country_bounds["max_lat"]

                    lon_span = max(max_lon - min_lon, 0.1)
                    lat_span = max(max_lat - min_lat, 0.1)

                    # small padding around the country

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

                    # fallback to coordinates in the dataset

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

                # build native echarts pie series for each city

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

                # normalize each metric separately to make all slices visible

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

                        # use a common scale for the visual pie slices

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
                        "formatter": JsCode(load_text_asset("js/geo_tooltip.js")).js_code
                    },
                    "geo": geo_options,
                    "series": pie_series
                }

                # recreate the chart when the country changes

                map_key = (
                    "geographical_sales_map_"
                    + normalize_geo_name(selected_country).replace(" ", "_")
                )

                render_streamlit_echarts(
                    options=map_options,
                    map=world_map,
                    height="550px",
                    key=map_key
                )

                # legend below the map

                render_html_template("geo_legend")

    # key performance indicators

    with kpi_col:
        st.markdown("**Key Metrics**")
        st.caption("")

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

        # colors matching the map legend

        metric_colors = {
            "Revenue": "#2A9D8F",
            "Profit": "#E9C46A",
            "Number of Orders": "#E76F51",
            "Units Sold": "#457B9D"
        }

        for metric in metric_cards:
            with st.container(border=True):
                st.markdown(f"**{metric['title']}**")
                render_metric_value(metric["value"])

                progress = min(
                    1.0,
                    max(0.0, float(metric["progress"]))
                )
                color = metric_colors[metric["title"]]

                render_progress_bar(progress=f"{progress * 100:.2f}", color=color)

    st.caption("")
    st.divider()
