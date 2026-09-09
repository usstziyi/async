import asyncio

class AsyncClass:
    def __init__(self, value):
        self.value = value
    
    def __await__(self):
        # 返回一个迭代器（通常是协程或 Future）
        async def _async_main():
            await asyncio.sleep(1)  # 模拟异步操作
            return self.value * 2
        
        return _async_main().__await__()

# 使用
async def main():
    obj = AsyncClass(10)
    result = await obj  # 直接 await 实例
    print(result)  # 20

    result = await obj  # 再次 await 实例，结果相同
    print(result)  # 20

asyncio.run(main())