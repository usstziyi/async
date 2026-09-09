import asyncio

async def my_coro():
    await asyncio.sleep(1)
    return 42

coro = my_coro()

# 1. 直接看属性
print(hasattr(coro, '__next__'))    # False (不是迭代器)
print(hasattr(coro, '__await__'))   # True  (是等待器)

# 2. 调用 __await__，获取迭代器
iterator = coro.__await__()
print(hasattr(iterator, '__next__')) # True (这就是图片里说的：返回值是迭代器)
print(type(iterator))               # <class 'coroutine_wrapper'> (是一个迭代器)


# 3. 手动驱动迭代器：每 next() 一次，协程就向前推进到下一个挂起点
# 但 my_coro 里的 asyncio.sleep(1) 必须运行在事件循环中，
# 用 next() 手动驱动会因为"没有运行中的事件循环"而报错：
try:
    next(iterator)  # RuntimeError: no running event loop
except RuntimeError as e:
    print(f"手动驱动失败: {type(e).__name__}: {e}")

# 4. 不依赖事件循环的协程，才能被 next() 手动驱动到结束。
# 结束后 next() 会抛 StopIteration，协程的返回值放在 e.value 里：
async def simple_coro():
    return 42

iterator2 = simple_coro().__await__()
try:
    next(iterator2)
except StopIteration as e:
    print("手动驱动完成, 返回值:", e.value)  # 42