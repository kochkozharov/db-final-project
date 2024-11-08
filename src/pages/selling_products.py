from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from services.sales import SalesService
from adapters.repositories.product import ProductRepository


def show_selling_products_page():
    # Хранение добавленных товаров в таблице
    if "sales_table" not in st.session_state:
        st.session_state.sales_table = pd.DataFrame(
            columns=["Название продукта", "Barcode", "Количество"]
        )

    if "products" not in st.session_state:
        st.session_state.products = ProductRepository().get_products()

    st.title("Продажа продуктов")

    # Получение даты
    date = st.date_input("Выберите дату", datetime.now())
    time = st.time_input("Выберите время", datetime.now(), step=timedelta(minutes=1))
    datetime_combined = datetime.combine(date, time)

    product_names = [product["name"] for product in st.session_state.products]
    product_barcodes = [product["barcode"] for product in st.session_state.products]

    # Поля для ввода данных
    selected_product = st.selectbox("Выберите продукт", product_names)
    quantity = st.number_input("Количество", min_value=1, max_value=100, value=1)

    # Найдем barcode выбранного продукта
    selected_product_barcode = product_barcodes[product_names.index(selected_product)]

    # Добавление товара в таблицу
    if st.button("Добавить продукт"):
        new_row = pd.DataFrame(
            {
                "Название продукта": [selected_product],
                "Barcode": [selected_product_barcode],
                "Количество": [quantity],
            }
        )
        st.session_state.sales_table = pd.concat(
            [st.session_state.sales_table, new_row], ignore_index=True
        )

    # Показать таблицу
    st.write("Добавленные товары:")
    st.dataframe(st.session_state.sales_table)

    if st.button("Очистить таблицу"):
        st.session_state.sales_table = pd.DataFrame(
            columns=["Название продукта", "Barcode", "Количество"]
        )
        st.rerun()

    if st.button("Подтвердить продажу") and len(st.session_state.sales_table) > 0:
        sale_id = SalesService().process_sale(
            datetime_combined,
            st.session_state.sales_table,
        )
        st.success(f"Продажа добавлена успешно! ID чека: {sale_id}")
