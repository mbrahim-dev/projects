# dataset overview page

import pandas as pd
import streamlit as st

def render_overview_page(df1: pd.DataFrame) -> None:
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