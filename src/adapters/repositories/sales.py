from adapters.repositories.base import BaseRepository
from pandas import DataFrame


class SalesRepository(BaseRepository):
    def add_sale(self, sale_date):
        query = """
            INSERT INTO sales (sale_date)
            VALUES (%s) RETURNING sale_id;
        """
        return self.fetchone(query, (sale_date,))

    def add_sale_details(self, sales: DataFrame):
        query = """
            INSERT INTO sales_details (sale_id, barcode, quantity)
            VALUES (%s, %s, %s);
        """
        self.executemany(
            query,
            sales[["sale_id", "barcode", "quantity"]].itertuples(
                index=False, name=None
            ),
        )

    def get_sales_statistics(self, grouping):
        query = """
            SELECT 
                date_trunc(%s, sale_date) as period, 
                SUM(revenue) as revenue,
                sum(quantity) AS quantity 
            FROM v_sales_statistics 
            GROUP BY period
        """
        return self.fetchall(query, (grouping,))
