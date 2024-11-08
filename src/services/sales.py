from datetime import datetime

from adapters.repositories.sales import SalesRepository
from pandas import DataFrame
import time


class SalesService:
    def __init__(self):
        self._repo: SalesRepository = SalesRepository()

    def process_sale(self, sale_date: datetime, items: DataFrame) -> int:
        time.sleep(10)
        items = items.rename(columns={"Количество": "quantity", "Barcode": "barcode"})
        items = items.groupby("barcode", as_index=False)["quantity"].sum()
        sale_id = self._repo.add_sale(sale_date)["sale_id"]

        items["sale_id"] = sale_id
        self._repo.add_sale_details(items)

        return sale_id
