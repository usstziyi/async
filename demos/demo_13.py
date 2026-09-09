import asyncio

# 为了让手动的 next() 能跑通，我们用一个普通的非异步挂起（yield）代替 asyncio.sleep
# async def my_coro():
#     await asyncio.sleep(1)  # 手动驱动这个会报错：await wasn't used with future
#     return 42

async def my_coro():
    await asyncio.sleep(0) # 换成 0 秒，或者干脆我们用个假数据模拟
    # 实际上，手动驱动原生协程往往会触发 RuntimeWarning: coroutine 'my_coro' was never awaited
    # 以及 RuntimeError: Task got bad yield
    return 42

coro = my_coro()

# 1. 直接看属性
print(f"是否有 __next__: {hasattr(coro, '__next__')}")    # False (不是迭代器)
print(f"是否有 __await__: {hasattr(coro, '__await__')}")   # True  (是等待器)

# 2. 调用 __await__，获取迭代器
iterator = coro.__await__()
print(f"__await__ 返回类型: {type(iterator)}")               # <class 'coroutine_wrapper'> (是一个迭代器)
print(f"返回的迭代器是否有 __next__: {hasattr(iterator, '__next__')}") # True

print("-" * 30)

# 3. 手动驱动它（模拟事件循环底层机制）
try:
    # 第一次调用 next，协程开始执行，直到遇到 await 挂起
    # 注意：这里会 yield 出一个 Future/Task 对象，并暂时停下来
    yielded_value = next(iterator) 
    print(f"第一次 next() 后，协程挂起，让出了: {type(yielded_value)}")

    # 在真实的事件循环中，循环会去处理这个 Future（比如等待 1 秒）
    # 处理完毕后，会通过 send(None) 把控制权交还给协程
    # 这里我们直接手动继续驱动它
    
    # 第二次调用 next，协程继续执行到结束
    # 正常情况下，遇到 return 42 会抛出 StopIteration
    try:
        next(iterator) 
    except StopIteration as e:
        print(f"第二次 next() 后，协程结束，返回值是: {e.value}")

except RuntimeError as e:
    print(f"驱动时遇到报错: {e}")
except Exception as e:
    print(f"驱动时遇到异常: {type(e).__name__}: {e}")