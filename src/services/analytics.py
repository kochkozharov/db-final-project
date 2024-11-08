from adapters.repositories.sales import SalesRepository
from pandas import DataFrame, to_datetime


class AnalyticsService:
    def __init__(self):
        self._repo: SalesRepository = SalesRepository()

    def get_sales_statistics(self, grouping: str) -> DataFrame:
        if grouping not in ["Day", "Week", "Month", "Year"]:
            raise ValueError("Invalid grouping")

        statistics = DataFrame(self._repo.get_sales_statistics(grouping))

        statistics["date"] = to_datetime(statistics["period"])

        return statistics[["date", "revenue", "quantity"]].set_index("date")
