"""demo_04：await 的真正价值 —— IO 密集场景对比

目标：前面都在用 asyncio.sleep 模拟。这里换成真实 IO（并发 HTTP 请求），
让你看到为什么 web/爬虫里 async 收益最大。

我们用同一个 httpx 库，对比"同步 client" vs "异步 client + gather"。
"""
import asyncio
import time

import httpx  # 已安装：uv add httpx

URLS = [
    "https://httpbin.org/delay/1",   # 服务端强制挂起返回
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

async def fetch(client: httpx.AsyncClient, url: str) -> tuple[int, str]:
    """异步请求一个 URL，返回 (状态码, url)。await 期间挂起，别的请求去发。"""
    resp = await client.get(url)
    return (resp.status_code, url)

async def async_requests_all() -> list[tuple[int, str]]:
    async with httpx.AsyncClient() as client:          # 异步上下文管理器
        tasks = [asyncio.create_task(fetch(client, u)) for u in URLS]
        return await asyncio.gather(*tasks)            # 4 个并发一起发

def sync_requests_all() -> list[tuple[int, str]]:
    with httpx.Client() as client:                     # 同步 client
        out = []
        for u in URLS:
            r = client.get(u)                          # 一个个来，阻塞等待
            out.append((r.status_code, u))
        return out


async def main():
    print("===== demo_04：真实 IO —— 同步 vs 异步并发 =====")

    # 同步版
    t0 = time.perf_counter()
    sync_results = sync_requests_all()
    t_sync = time.perf_counter() - t0
    print(f"  同步 httpx     : {t_sync:.2f}s   结果数={len(sync_results)}")

    # 异步版
    t0 = time.perf_counter()
    async_results = await async_requests_all()
    t_async = time.perf_counter() - t0
    print(f"  异步 httpx     : {t_async:.2f}s   结果数={len(async_results)}")

    print(f"\n  加速比 ≈ {t_sync / t_async:.1f}x  （请求越多、延迟越高，收益越大）")
    print("  原因：等待 IO 返回的空档期，CPU 没闲着，而是去处理其它协程。")


if __name__ == "__main__":
    asyncio.run(main())