from asyncio import run, wait, create_task
from asyncpg import create_pool, Pool

from utils.python.config import config_postgres
from utils.python.util import async_time


async def query(pool: Pool):
    async with pool.acquire() as connection:
        return await connection.fetch(config_postgres.query)

@async_time()
async def main():
    async with create_pool(host=config_postgres.host,
                                   port=config_postgres.port,
                                   user=config_postgres.user,
                                   password=config_postgres.passwd,
                                   database=config_postgres.database,
                                   min_size=config_postgres.max_query,
                                   max_size=config_postgres.max_query) as pool:
        
        tasks = [create_task(query(pool)) for i in range(config_postgres.N)]
        done, _ = await wait(tasks)
        exceptions = [res for res in done if res.exception() is not None]
        print(f"Async requests done: {len(done)}, exceptions: {len(exceptions)}, requests at all {config_postgres.N}")



if __name__ == "__main__":
    run(main())
