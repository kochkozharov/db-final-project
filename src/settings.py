import os
from dotenv import load_dotenv
import redis

load_dotenv(".env")

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)
redis_client = redis.Redis(connection_pool=redis_pool)

POOL_MIN_CONN = int(os.getenv("POOL_MIN_CONN", 1))
POOL_MAX_CONN = int(os.getenv("POOL_MAX_CONN", 10))