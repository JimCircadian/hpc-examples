import asyncio
import concurrent.futures as cf
import datetime as dt
import os
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
    await asyncio.sleep(2)
    print("End {}".format(i))


# Thank you: https://stackoverflow.com/questions/16071866/non-blocking-subprocess-call
async def async_cmd(i):
    print("Started {}".format(i))
    proc = await asyncio.create_subprocess_exec('sleep', '2')
    rc = await proc.wait()
    print("End {}".format(i))


async def async_bash(i):
    print("Started {}".format(i))
    proc = await asyncio.create_subprocess_shell('./sleep.sh {}'.format(i), cwd="subdir")
    rc = await proc.wait()
    print("End {}".format(i))


def batch_runs(loop, func):
    tasks = list()

    for i in range(10):
        tasks.append(func(i))

    loop.run_until_complete(sem_batcher(15, tasks))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].startswith("async_") and \
            hasattr(sys.modules['__main__'], sys.argv[1]):
        func = getattr(sys.modules['__main__'], sys.argv[1])
    else:
        func = async_cmd

    print("""asyncio semaphore limiter test {}""".format(func.__name__))

    # timeit seems to get a bit grumpy
    st = dt.datetime.now()
    num = 5
    loop = asyncio.get_event_loop()

    try:
        # with cf.ThreadPoolExecutor() as executor:
        #     for i in range(num):
        #         futures = executor.submit(batch_runs, loop, func)
        # cf.as_completed(futures)

        # This will allow sequential execution of "batches", but not parallelised as above which only runs asyncio
        # TODO: BUT I cannot find a reliable description of the inheritence of process to subprocess cwd....
        #  This is what i want to test!
        for i in range(num):
            orig = os.getcwd()
            batch_runs(loop, func)
            os.chdir(orig)

    finally:
        loop.shutdown_asyncgens()
        loop.close()

    en = dt.datetime.now()
    print("Elapsed: {} seconds".format((en - st).total_seconds()))

