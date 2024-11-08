from adapters.repositories.base import BaseRepository
from pandas import DataFrame


class DeliveryRepository(BaseRepository):
    def add_delivery(self, supplier_id, delivery_date):
        query = """
            INSERT INTO deliveries (supplier_id, delivery_date)
            VALUES (%s, %s) RETURNING delivery_id;
        """
        return self.fetchone(query, (supplier_id, delivery_date))

    def add_delivery_contents(self, delivery: DataFrame):
        query = """
            INSERT INTO delivery_contents (delivery_id, barcode, quantity)
            VALUES (%s, %s, %s);
        """
        self.executemany(
            query,
            delivery[["delivery_id", "barcode", "quantity"]].itertuples(
                index=False, name=None
            ),
        )
