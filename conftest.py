import asyncio


async def say_hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")


asyncio.run(say_hello())