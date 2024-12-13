from settings import DB_CONFIG
import psycopg2


def execute_query(query: str, params=None):
    """Executes a query on the database."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT") or query.split()[-2].upper() == "RETURNING":
                return cursor.fetchall()
            conn.commit()
            return