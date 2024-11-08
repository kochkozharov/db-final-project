from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from adapters.repositories.suppliers import SuppliersRepository
from services.delivery import DeliveryService


def show_delivery_page():
    if "suppliers" not in st.session_state:
        st.session_state.suppliers = SuppliersRepository().get_suppliers()

    st.title("Поставка продуктов")

    # Получение даты
    date = st.date_input("Выберите дату", datetime.now())

    # Получение времени
    time = st.time_input("Выберите время", datetime.now(), step=timedelta(minutes=1))

    # Объединение даты и времени
    datetime_combined = datetime.combine(date, time)

    # Поле для выбора поставщика
    suppliers = st.session_state.suppliers
    supplier_id = st.selectbox(
        "Имя поставщика",
        options=[supplier["supplier_id"] for supplier in suppliers],
        format_func=lambda id: next(
            supplier["name"] for supplier in suppliers if supplier["supplier_id"] == id
        ),
    )

    # Поле для загрузки CSV файла
    uploaded_file = st.file_uploader(
        "Загрузите CSV-файл с данными о доставке", type=["csv"]
    )

    # Обработка загруженного файла
    if uploaded_file:
        delivery_data = pd.read_csv(uploaded_file)
        st.write("Загруженные данные о доставке:")
        st.write(delivery_data)

    # Кнопка подтверждения доставки
    if st.button("Подтвердить доставку"):
        if uploaded_file:
            # Проверка структуры CSV (например, наличие колонок 'barcode' и 'quantity')
            if (
                "barcode" in delivery_data.columns
                and "quantity" in delivery_data.columns
            ):
                delivery_id = DeliveryService().upload_delivery(
                    delivery_data, supplier_id, datetime_combined
                )
                st.success(f"Доставка добавлена успешно! ID доставки: {delivery_id}")
            else:
                st.error("Файл CSV должен содержать колонки 'barcode' и 'quantity'")
        else:
            st.error("Загрузите CSV файл с данными о доставке")
