# use wait
from asyncio import run, create_task, wait
from aiohttp import ClientSession, ClientTimeout

from utils.python.util import async_time
from utils.python.config import config_http


async def request(session: ClientSession, url: str):
    async with session.get(url) as result:
        resp = result.status
    
    return resp


@async_time()
async def main():
    client_timeout = ClientTimeout(total=10, connect=10)
    session = ClientSession(timeout=client_timeout)
    tasks = [create_task(request(session, config_http.URL)) for i in range(config_http.N)]
    done, _ = await wait(tasks)
    exceptions = [res for res in done if res.exception() is not None]
    print(f"Async requests done: {len(done)}, exceptions: {len(exceptions)}, requests at all {config_http.N}")
    await session.close()



if __name__ == "__main__":
    run(main())
