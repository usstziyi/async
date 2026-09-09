import asyncio
import inspect  # 用来查看协程状态

async def foo():
    await asyncio.sleep(0.1)
    return 42

async def main():
    coro = foo()  # 创建协程对象
    
    # 初始状态：已创建
    print(inspect.getcoroutinestate(coro))  # CORO_CREATED
    
    # 第一次await：正常执行
    res1 = await coro
    print(res1)  # 42
    
    # 执行完毕后状态：已关闭
    print(inspect.getcoroutinestate(coro))  # CORO_CLOSED
    
    # 第二次await：直接报错
    res2 = await coro  # RuntimeError: cannot reuse already awaited coroutine

asyncio.run(main())
