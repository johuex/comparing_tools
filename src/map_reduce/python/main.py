from concurrent.futures import ProcessPoolExecutor
import functools
import asyncio
from io import TextIOWrapper
from multiprocessing import Value
import os
from typing import List, Dict
from utils.python.util import async_time

map_progress: Value
CHUNK_SIZE = 2000000  # lines for one read operation

def init(progress: Value):
    global map_progress
    map_progress = progress


def merge_dictionaries(first: Dict[str, int],
                       second: Dict[str, int]) -> Dict[str, int]:
    """
    Функция редукции: слияние словарей
    """
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter

def get_chunk(fileobj: TextIOWrapper):
    while chunk := fileobj.readlines(CHUNK_SIZE):
        if not len(chunk):
            return
        yield chunk

async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f'Finished {map_progress.value}/{total_partitions} map operations')
        await asyncio.sleep(1)

def lines_count(fileobj: TextIOWrapper):
    lines = 0
    buf_size = 1024 * 1024
    read_f = fileobj.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines

@async_time()
async def main():
    global map_progress

    with open('./src/map_reduce/googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as fileobj:
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value('i', 0)
        final_result = {}

        with ProcessPoolExecutor(initializer=init,
                                 initargs=(map_progress,)) as pool:
            total_partitions = lines_count(fileobj) // CHUNK_SIZE
            fileobj.seek(0)  # set cursor to start of file
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            while True:
                i = 0
                for chunk in get_chunk(fileobj):
                    i += 1
                    tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies, chunk)))
                    if i == os.cpu_count():
                        i = 0
                        break
                if not tasks:
                    break
                counters = await asyncio.gather(*tasks)
                final_result = merge_dictionaries(final_result, functools.reduce(merge_dictionaries, counters))
                tasks = []


            await reporter

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")


if __name__ == "__main__":
    asyncio.run(main())
