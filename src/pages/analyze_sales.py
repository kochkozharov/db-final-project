import streamlit as st
from services.analytics import AnalyticsService
from datetime import datetime, timedelta


def change_grouping(grouping):
    if "grouping" not in st.session_state:
        st.session_state.analysis_data = AnalyticsService().get_sales_statistics(
            grouping
        )
        st.session_state.grouping = grouping
        st.session_state.grouping_updated_at = datetime.now()
    elif (
        st.session_state.grouping != grouping
        or st.session_state.grouping_updated_at
        < (datetime.now() - timedelta(minutes=1))
    ):
        st.session_state.analysis_data = AnalyticsService().get_sales_statistics(
            grouping
        )
        st.session_state.grouping = grouping
        st.session_state.grouping_updated_at = datetime.now()


# Page 3: Analyze Sales
def show_analyze_sales_page():
    if "analysis_data" not in st.session_state:
        change_grouping("Day")

    st.title("Анализ продаж")

    grouping = st.selectbox(
        "Group by",
        ["Day", "Week", "Month", "Year"],
    )
    change_grouping(grouping)

    display_option = st.radio("Display as", ["Table", "Chart"])
    if display_option == "Table":
        st.dataframe(st.session_state.analysis_data)
    else:
        st.line_chart(st.session_state.analysis_data["revenue"])
        print("1")
