import asyncpg

DATABASE_URL = (

)

class Asyncpg:
    _instance = None
    _pool: asyncpg.Pool | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Asyncpg, cls).__new__(cls)
        return cls._instance
    
    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                dsn=DATABASE_URL,
                min_size=1,
                max_size=10
            )
        if self._pool is None:
            raise ValueError("Could not connect to Postgres")
    
    async def get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise ValueError('Could not get pool')
        return self._pool

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None