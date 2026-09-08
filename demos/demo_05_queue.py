"""demo_05：asyncio.Queue —— 生产者/消费者模式

目标：这是 async 工程里最常用的协作模式。生产者和消费者通过队列解耦，
队列天然是异步安全（单线程内非 goroutine）的。

场景：一个订单流水 → 多个处理工位并行消化。
"""
import asyncio
import random


async def producer(queue: asyncio.Queue[str], total: int):
    """只负责把 total 个订单放进队列，不关心谁消费。"""
    for i in range(1, total + 1):
        item = f"订单-{i:02d}"
        await queue.put(item)                       # 队列满了会自动挂起等待（背压）
        print(f"  [生产者]  放入 {item}")
        await asyncio.sleep(random.uniform(0.01, 0.05))
    print(f"  [生产者]  生产完毕，共 {total} 单")


async def consumer(name: str, queue: asyncio.Queue[str]):
    """从队列取订单处理。遇到哨兵 None 就下班。"""
    while True:
        order = await queue.get()                   # 队列为空时挂起等待
        if order is None:
            print(f"  [消费者{name}] 收到结束信号，下班。")
            break
        print(f"  [消费者{name}] 开始加工 {order} …")
        await asyncio.sleep(random.uniform(0.1, 0.4))   # 模拟处理耗时
        queue.task_done()                           # 向队列汇报：这条已处理完
        print(f"  [消费者{name}] 完成 {order}")


async def stop_workers(queue: asyncio.Queue[str], n_workers: int):
    """给每个消费者各放一个 None 哨兵，保证它们都能退出。"""
    for _ in range(n_workers):
        await queue.put(None)


async def main():
    total = 8
    n_workers = 3
    q: asyncio.Queue[str] = asyncio.Queue(maxsize=3)  # 容量 3，体会背压

    print(f"===== demo_05：{n_workers} 个工位并发消化 {total} 个订单 =====")

    workers = [asyncio.create_task(consumer(f"W{i}", q)) for i in range(1, n_workers + 1)]

    await producer(q, total)
    await q.join()                                  # 等所有订单都被 task_done() 处理完
    print("  [主流程]  全部订单已消化完毕")

    await stop_workers(q, n_workers)                # 收工前发 N 个哨兵
    await asyncio.gather(*workers)

    print("\n核心理解：producer 只管放置、consumer 只管消费，二者用 Queue 解耦，"
          "并通过 await 自动协调快慢（低速不会拖垮高速）。")


if __name__ == "__main__":
    asyncio.run(main())