from adapters.repositories.base import BaseRepository


class SuppliersRepository(BaseRepository):
    def get_suppliers(self):
        query = "SELECT supplier_id, name, phone, address FROM suppliers;"
        return self.fetchall(query)
