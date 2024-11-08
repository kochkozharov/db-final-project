from adapters.connector import get_connection
from typing import Any, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BaseRepository:
    def execute(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                logger.info(f"Executing query: {query} with params: {params}")
                cursor.execute(query, params)
                conn.commit()

    def executemany(self, query: str, params: List[Tuple[Any, ...]]) -> None:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                logger.info(f"Executing batch query: {query} with params: {params}")
                cursor.executemany(query, params)
                conn.commit()

    def fetchall(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> List[Tuple[Any, ...]]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                logger.info(
                    f"Fetching all rows with query: {query} and params: {params}"
                )
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def fetchone(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> Optional[Tuple[Any, ...]]:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                logger.info(
                    f"Fetching one row with query: {query} and params: {params}"
                )
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                result = dict(zip(columns, cursor.fetchone()))
                conn.commit()
                return result
