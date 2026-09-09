import asyncio

async def my_coro():
    return 42

coro = my_coro()  # 原生协程对象

# 直接调用 next(coro) 会报错：原生协程不是迭代器
# next(coro)  # TypeError: 'coroutine' object is not an iterator

# 调用 __await__() 拿到驱动迭代器
it = coro.__await__()
print(type(it))  # <class 'coroutine_wrapper'>

# 这个迭代器完全符合迭代器协议，可以正常 next
try:
    next(it)
except StopIteration as e:
    print(f"协程结束，返回值：{e.value}")  # 输出：协程结束，返回值：42
