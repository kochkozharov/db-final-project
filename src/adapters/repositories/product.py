from adapters.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def get_products(self):
        query = "SELECT barcode, name FROM products;"
        return self.fetchall(query)
