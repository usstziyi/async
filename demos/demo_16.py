import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)  # 第1个暂停点
    print("World")
    return "Done"

coro = hello()
gen = coro.__await__()

# 第1次推动：启动协程
future = gen.send(None)  # 打印 "Hello"，返回一个 Future 对象
print(f"协程暂停在 await，交出控制权，给了我们一个 {type(future).__name__}")

# 模拟等待1秒
import time
time.sleep(1)

# 第2次推动：继续执行
try:
    gen.send(None)  # 打印 "World"，然后抛 StopIteration
except StopIteration as e:
    print(f"协程完成，返回值: {e.value}")