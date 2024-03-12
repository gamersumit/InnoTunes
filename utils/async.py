import asyncio

async def say_hello(delay, name):
    await asyncio.sleep(delay)
    print(f"Hello, {name}!")

async def main():
    # Create tasks
    task1 = asyncio.create_task(say_hello(10, "Alice"))
    task2 = asyncio.create_task(say_hello(2, "Bob"))

    # Wait for all tasks to complete
    await asyncio.gather(task1, task2)

asyncio.run(main())
