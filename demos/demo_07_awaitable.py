"""demo_07：可等待对象（awaitable）到底有哪些

目标：验证上一轮讲的概念——
  1) 三种标准 awaitable：协程 / Task / Future
  2) 自定义 awaitable：实现 __await__ 的对象
  3) 常见错误：哪些不能 await

运行：uv run python demos/demo_07_awaitable.py
"""
import asyncio


# ---- 1) 一个普通 async 函数 —— 产生"协程" ----
async def fetch(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"{name} 返回了，花了 {seconds}s"


# ---- 2) 自定义可等待对象：实现 __await__ ----
class AutoCook:
    """一个无需手动 await 的"自动做菜"：实现 __await__ 后，能放在 await 后面。"""

    def __init__(self, name: str, seconds: float):
        self.name = name
        self.seconds = seconds

    def __await__(self):
        # 协程需要调用自己的 .__await__() 才会被包装成符合要求的迭代器。
        return self._run().__await__()

    async def _run(self) -> str:
        await asyncio.sleep(self.seconds)
        return f"{self.name}（自定义 awaitable）出锅！"


async def main():
    print("===== demo_07a：三种标准 awaitable 都能 await =====")

    # 1) 协程：直接 await async 函数"调用后"的对象
    r_coro = await fetch("协程", 0.3)
    print("  协程 :", r_coro)

    # 2) Task：用 create_task 包一层，交给事件循环并发调度
    task = asyncio.create_task(fetch("Task", 0.3))
    r_task = await task
    print("  Task :", r_task)

    # 3) Future：底层占位符，Task 是它的子类。手动造一个在别处完成。
    fut = asyncio.get_event_loop().create_future()
    loop = asyncio.get_event_loop()

    async def fill_future():
        await asyncio.sleep(0.2)
        fut.set_result("Future 的值" if not fut.done() else "already done")
        return None

    asyncio.create_task(fill_future())
    r_fut = await fut
    print("Future:", r_fut)

    print("\n===== demo_07b：并发跑多个自定义 awaitable =====")
    dishes = [AutoCook("糖醋鱼", 0.4), AutoCook("宫保鸡丁", 0.5), AutoCook("麻婆豆腐", 0.2)]
    results = await asyncio.gather(*dishes)  # gather 内部把它们当协程并发调度
    for r in results:
        print("  ", r)
    print(f"  总耗时约 {0.5:.2f}s（≈最慢那道菜，而不是 0.4+0.5+0.2）")

    print("\n===== demo_07c：常见错误示范（会抛异常） =====")
    await demo_errors()


async def demo_errors():
    async def crash1():
        # 错误1：await 一个"未调用的 async 函数名"
        return await fetch          # TypeError

    async def crash2():
        # 错误2：await 一个非 awaitable（普通数字）
        return await 123            # 同理无法 await 数字

    for label, coro in [("await 函数名(少括号)", crash1()), ("await 非awaitable(数字)", crash2())]:
        try:
            await coro
            print(f"  [意外] {label} 竟然成功")
        except TypeError as e:
            print(f"  [预期异常] {label} -> {type(e).__name__}: {str(e)[:36]}...")


if __name__ == "__main__":
    asyncio.run(main())