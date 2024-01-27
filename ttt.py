import asyncio


async def my_task1(task_name, seconds):
    """
    This is an example coroutine that takes a name and a number of seconds
    as input, and waits for that many seconds before returning a message.
    """
    print(f"{task_name} started")
    await asyncio.sleep(seconds)  # This simulates some work being done
    print(f"{task_name} finished")
    return f"{task_name} completed in {seconds} seconds"


async def my_task2(task_name, seconds):
    while True:
        print(f"{task_name}")
        await asyncio.sleep(seconds)  # This simulates some work being done


async def main():
    """
    This is the main coroutine that creates and runs several subtasks in parallel.
    """
    # Create a list of tasks to run concurrently
    tasks = [
        asyncio.create_task(my_task1("Task 1", 1)),
        asyncio.create_task(my_task2("Task 2", 0.1)),
    ]

    # Wait for all tasks to complete and retrieve their results
    results = await asyncio.gather(*tasks)
    print(results)


# Run the main coroutine in the asyncio event loop
asyncio.run(main())
