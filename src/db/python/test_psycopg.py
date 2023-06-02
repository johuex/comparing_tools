from asyncio import AbstractEventLoop, run, wait, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List
from psycopg2.pool import ThreadedConnectionPool

from utils.python.config import config_postgres
from utils.python.util import async_time


def query(pool: ThreadedConnectionPool):
    connection = pool.getconn()
    try:
        cursor = connection.cursor()
        cursor.execute(config_postgres.query)
    except Exception:
        pass
    finally:
        # return connection to pool
        pool.putconn(connection)


def get_pool() -> ThreadedConnectionPool:
    pool = ThreadedConnectionPool(
        minconn=config_postgres.max_query,
        maxconn=config_postgres.max_query,
        host=config_postgres.host,
        port=config_postgres.port,
        user=config_postgres.user,
        password=config_postgres.passwd,
        database=config_postgres.database
    )
    return pool


@async_time()
async def main_thread_and_asyncio():
    # ThreadPool + asyncio
    with ThreadPoolExecutor(max_workers=config_postgres.max_query) as thread_pool:
        loop: AbstractEventLoop = get_running_loop()
        pool = get_pool()
        calls: List = [partial(query, pool) for i in range(config_postgres.N)]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(thread_pool, call))

        done, _ = await wait(call_coros)
        exceptions = [res for res in done if res.exception() is not None]
        
    print(f"Sync requests done: {len(done)}, exceptions: {len(exceptions)}, requests at all {config_postgres.N}")
    if len(exceptions):
        await exceptions[1]


@async_time()
async def main_thread_only():
    # ThreadPool only
    with ThreadPoolExecutor(max_workers=config_postgres.max_query) as thread_pool:
        pool = get_pool()
        pools = [pool for i in range(config_postgres.N)]
        results = list(thread_pool.map(query, pools))
        exceptions = [res for res in results if type(res) is Exception]
        
    print(f"Sync requests done: {len(results)}, exceptions: {len(exceptions)}, requests at all {config_postgres.N}")
    if len(exceptions):
        await exceptions[1]


if __name__ == "__main__":
    run(main_thread_and_asyncio())
    #run(main_thread_only())
