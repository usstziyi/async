import asyncio

async def foo():
    print("run foo")
    return 10

async def main():
    coro = foo()
    res1 = await coro
    print(res1)
    res2 = await coro  # ❌ 报错：cannot reuse already awaited coroutine
    print(res2)

if __name__ == "__main__":
    asyncio.run(main())
