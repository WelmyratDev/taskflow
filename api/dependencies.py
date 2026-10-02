from infrastructure.asyncpg import Asyncpg
import asyncpg


async def inject_apg_pool() -> asyncpg.Pool:
    pg = Asyncpg()
    await pg.connect()
    pg_pool = await pg.get_pool()
    return pg_pool
    
