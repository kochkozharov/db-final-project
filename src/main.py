from pages.delivery import show_delivery_page
from pages.selling_products import show_selling_products_page
import streamlit as st
from pages.analyze_sales import show_analyze_sales_page


# Главная логика приложения с навигацией
def main():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Перейти к странице",
        ["Доставка продуктов", "Продажа продуктов", "Анализ продаж"],
    )

    if page == "Доставка продуктов":
        show_delivery_page()
    elif page == "Продажа продуктов":
        show_selling_products_page()
    elif page == "Анализ продаж":
        show_analyze_sales_page()


if __name__ == "__main__":
    main()
