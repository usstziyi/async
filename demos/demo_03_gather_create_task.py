"""demo_03：并发魔法 —— asyncio.gather / create_task

目标：真正把 3 道菜"同时"开做。

两种方式：
  1) asyncio.gather(a, b, c)      —— 一次并发跑一批，等全部完成
  2) asyncio.create_task(fn())    —— 把一个协程"排入后台"，主协程继续往前走

注意：并发 ≠ 并行。
  - 并发（concurrency）：一个 CPU 同时"管理"多个任务，靠挂起/切换，适合 IO 密集。
  - 并行（parallelism）：多核同时跑多个任务，asyncio 单线程里并不做这个。
"""
import asyncio
import random


async def cook(name: str, seconds: float, tag: str) -> str:
    print(f"    [{tag}] 开做 [{name}]，{seconds}s ...")
    await asyncio.sleep(seconds)
    return f"    [{tag}] [{name}] 完成度 100%！"

async def order(name: str, seconds: float, tag: str) -> str:
    """模拟点单：随机等待一下，让并发时序更清晰。"""
    wait = random.uniform(0.05, 0.2)
    await asyncio.sleep(wait)
    return await cook(name, seconds, tag)


async def main():
    start = asyncio.get_event_loop().time()

    # ---- 方式 1：gather 一把梭 ----
    print("===== A) asyncio.gather：同时开做，全部完成后统一拿结果 =====")
    dishes = [
        order("西红柿", 1.0, "A"),
        order("土豆", 2.0, "B"),
        order("牛肉", 3.0, "C"),
    ]
    results = await asyncio.gather(*dishes)
    for r in results:
        print(r)
    print(f"    gather 总耗时：{asyncio.get_event_loop().time() - start:.2f}s（≈ 最慢那道菜，而非累加！）\n")

    # ---- 方式 2：create_task 边做边等 ----
    start = asyncio.get_event_loop().time()
    print("===== B) create_task：启动后台任务，主协程手里继续忙别的 =====")
    t1 = asyncio.create_task(cook("蒜蓉虾", 1.5, "X"))
    t2 = asyncio.create_task(cook("椒盐蟹", 2.0, "Y"))
    print("    后台已在做两道菜，主协程先打印点东西：")
    await asyncio.sleep(0.3)
    print("    主协程：擦桌子、摆碗筷...")
    # 最后等所有 task 结束（create_task 不会自动等待，必须 await）
    await asyncio.gather(t1, t2)
    print(f"    create_task 总耗时：{asyncio.get_event_loop().time() - start:.2f}s")

    print("\n核心理解：总耗时 = 最慢任务的耗时，而不是所有任务耗时之和。")


if __name__ == "__main__":
    asyncio.run(main())