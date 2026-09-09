"""demo_06：异步生成器 + 异步上下文管理器

目标：两个高频但易被忽略的异步机制：

  1) async for  —— 异步生成器，边产出边等待，适合流式读取/分页爬取。
  2) async with —— 异步上下文管理器，__aenter__/__aexit__ 里可 await，
                   典型场景：打开/关闭连接、网络会话。

用"分页抓取日志"的模拟场景把它们串起来。
"""
import asyncio


# ---- 异步上下文管理器：模拟一个可开/关的数据库连接 ----
class DBConnection:
    async def __aenter__(self):
        print("  [连接] 正在建立数据库连接...")
        await asyncio.sleep(0.2)
        print("  [连接] 已连接。")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("  [连接] 正在断开连接...")
        await asyncio.sleep(0.1)
        print("  [连接] 已断开。")
        return False  # False = 不吞掉异常

    async def query(self, sql: str) -> str:
        await asyncio.sleep(0.1)
        return f"结果({len(sql)} chars): {sql}"


# ---- 异步生成器：边 await 边 yield，模拟分页拉取 ----
async def page_fetcher(pages: int):
    """每个 page 之间会 await，从第 1 页吐到第 pages 页。"""
    for i in range(1, pages + 1):
        await asyncio.sleep(0.1)                       # 模拟网络往返
        yield f"<log-page-{i}> ..."                    # yield 一页数据


async def main():
    print("===== demo_06a：async with 连接管理 =====")
    async with DBConnection() as db:
        r1 = await db.query("SELECT * FROM users")
        r2 = await db.query("SELECT * FROM orders")
        print(f"  {r1}")
        print(f"  {r2}")
    print("  （退出 async with 后，连接自动关闭）\n")

    print("===== demo_06b：async for 流式消费 =====")
    async for page in page_fetcher(4):
        print(f"  拿到一页日志")

    print("\n核心理解：")
    print("  - async with：让'打开-使用-关闭'这段需要 await 的资源管理变得安全整洁。")
    print("  - async for  ：每次迭代都可能 await，适合数据不是一次性到齐的场景。")

if __name__ == "__main__":
    asyncio.run(main())