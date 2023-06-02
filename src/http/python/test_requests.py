from asyncio import AbstractEventLoop, run, get_running_loop, wait
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List
import requests

from utils.python.config import config_http
from utils.python.util import async_time, sync_time

def request(url: str):
    session = requests.session()
    res = session.get(url)
    assert res.status_code == 200
    return res.status_code


@async_time()
async def main_thread_and_asyncio():
    # ThreadPool + asyncio
    with ThreadPoolExecutor(max_workers=config_http.max_request) as thread_pool:
        loop: AbstractEventLoop = get_running_loop()
        calls: List = [partial(request, config_http.URL) for i in range(config_http.N)]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(thread_pool, call))

        done, _ = await wait(call_coros)
        exceptions = [res for res in done if res.exception() is not None]
        if len(exceptions):
            await exceptions[0]
        
    print(f"Sync requests done: {len(done)}, exceptions: {len(exceptions)}, requests at all {config_http.N}")


@sync_time()
def main_thread_only():
    # ThreadPool only
    with ThreadPoolExecutor(max_workers=config_http.max_request) as pool:
        urls = [config_http.URL for _ in range(config_http.N)]
        results = list(pool.map(request, urls))
        exceptions = [res for res in results if type(res) is Exception]
    
    print(f"Sync requests done: {len(results)}, exceptions: {len(exceptions)}, requests at all {config_http.N}")


if __name__ == "__main__":
    run(main_thread_and_asyncio())
    #run(main_thread_only())
