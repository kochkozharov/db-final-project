from datetime import datetime

from adapters.repositories.delivery import DeliveryRepository
from pandas import DataFrame


class DeliveryService:
    def __init__(self):
        self._repo: DeliveryRepository = DeliveryRepository()

    def upload_delivery(
        self, delivery_data: DataFrame, supplier_id: int, delivery_date: datetime
    ) -> int:
        delivery_id = self._repo.add_delivery(supplier_id, delivery_date)["delivery_id"]

        delivery_data["delivery_id"] = delivery_id
        self._repo.add_delivery_contents(delivery_data)

        return delivery_id
