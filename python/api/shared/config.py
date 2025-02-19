import os

import asyncpg
from asyncpg import Pool

DB_NAME = os.getenv("DB_NAME", "rinha")
DB_USERNAME = os.getenv("DB_USERNAME", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_HOST = os.getenv("DB_HOST", "postgresdb")
DB_MAX_CONNECTIONS = int(os.getenv("DB_MAX_CONNECTIONS", "4"))

CONNECTION_POOL = None


async def get_connection_pool() -> Pool:
    global CONNECTION_POOL
    if not CONNECTION_POOL:
        CONNECTION_POOL = await asyncpg.create_pool(user=DB_USERNAME, database=DB_NAME, host=DB_HOST,
                                                    port=DB_PORT, password=DB_PASSWORD,
                                                    min_size=DB_MAX_CONNECTIONS - 1,
                                                    max_size=DB_MAX_CONNECTIONS)
    return CONNECTION_POOL
