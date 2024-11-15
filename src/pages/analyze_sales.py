from datetime import date

import pandas as pd

import streamlit as st
from services.sales import SalesService
import repositories.products
from repositories.sales import get_sales_statistics


@st.cache_data
def get_products() -> dict[str, str]:
    print("Получение продуктов")
    products = repositories.products.get_products()

    return {product["name"]: product["barcode"] for product in products}


products = get_products()


def show_analyze_sales_page():
    st.title("Анализ продаж")

    selected_product = st.selectbox("Выберите продукт", products.keys())

    display_option = st.radio("Display as", ["Table", "Chart"])

    if selected_product:
        selected_product_barcode = products[selected_product]
        sales = get_sales_statistics(selected_product_barcode)
        if len(sales) == 0:
            st.warning("Нет продаж для выбранного продукта")
        else:
            if display_option == "Table":
                st.dataframe(sales)
            else:
                if len(sales) == 1:
                    st.warning("Только одна продажа...")
                else:
                    st.line_chart(sales, x="sale_date", y="quantity")
