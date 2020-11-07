import asyncio
import datetime as dt
import sys


# Thank you: https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio/61478547#61478547
async def sem_batcher(n, tasks):
    sem = asyncio.Semaphore(n)

    async def sem_task(task):
        async with sem:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def async_sleep(i):
    print("Started {}".format(i))
    # This doesn't block
    await asyncio.sleep(5)
    print("End {}".format(i))


# Thank you: https://stackoverflow.com/questions/16071866/non-blocking-subprocess-call
async def async_cmd(i):
    print("Started {}".format(i))
    # But this does, what can I do
    proc = await asyncio.create_subprocess_exec('sleep', '5')
    rc = await proc.wait()
    print("End {}".format(i))


def batch_runs(func):
    tasks = list()

    loop = asyncio.get_event_loop()

    for i in range(50):
        tasks.append(func(i))

    try:
        loop.run_until_complete(sem_batcher(15, tasks))
    finally:
        loop.shutdown_asyncgens()
        loop.close()


if __name__ == "__main__":
    print("""asyncio semaphore limiter test""")

    if len(sys.argv) == 2 and sys.argv[1] == "asyncio":
        func = async_sleep
    else:
        func = async_cmd

    # timeit seems to get a bit grumpy
    st = dt.datetime.now()
    batch_runs(func)
    en = dt.datetime.now()
    print("Elapsed: {} seconds".format((en - st).total_seconds()))

