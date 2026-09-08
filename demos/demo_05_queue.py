"""demo_05：asyncio.Queue —— 生产者/消费者模式

目标：这是 async 工程里最常用的协作模式。生产者和消费者通过队列解耦，
队列天然是异步安全（单线程内非 goroutine）的。

场景：一个订单流水 → 多个处理工位并行消化。
"""
import asyncio
import random


async def producer(queue: asyncio.Queue[str], count: int):
    """不断往队列里放订单。"""
    for i in range(1, count + 1):
        order = f"订单-{i:02d}"
        await queue.put(order)                      # 队列已满时会挂起等待
        print(f"  [生产者]  放入了 {order}")
        await asyncio.sleep(random.uniform(0.02, 0.08))
    await queue.put(None)                           # 哨兵：通知消费者结束
    print("  [生产者]  生产完毕，发出结束信号")


async def consumer(name: str, queue: asyncio.Queue[str]):
    """从队列取订单处理。识别到哨兵 None 则退出。"""
    while True:
        order = await queue.get()                   # 队列为空时会挂起等待
        if order is None:
            print(f"  [消费者{name}] 收到结束信号，下班。")
            break
        print(f"  [消费者{name}] 正在加工 {order} …")
        await asyncio.sleep(random.uniform(0.1, 0.4))   # 模拟处理耗时
        queue.task_done()                           # 标记本条处理完成
        print(f"  [消费者{name}] 完成 {order}")


async def main():
    q: asyncio.Queue[str] = asyncio.Queue(maxsize=3)  # 队列最多放 3 个，体会背压

    print("===== demo_05：生产者/消费者（3 个工位并发消化 8 个订单） =====")
    # 注意：producer 只产生一个结束信号，但 3 个消费者都在等 —— 这里简化：生产数量=8，
    # 用多个哨兵保证每个消费者都能退出（教学示例，用简单计数法）
    total = 8
    n_workers = 3

    # 教学版：放 total 个真实订单 + n_workers 个结束哨兵
    async def producer_full():
        for i in range(1, total + 1):
            item = f"订单-{i:02d}"
            await q.put(item)
            print(f"  [生产者]  放入 {item}")
            await asyncio.sleep(random.uniform(0.01, 0.05))
        for _ in range(n_workers):
            await q.put(None)

    workers = [asyncio.create_task(consumer(f"W{i}", q)) for i in range(1, n_workers + 1)]
    await producer_full()
    await asyncio.gather(*workers)

    print("\n核心理解：producer 只管放置、consumer 只管消费，二者用 Queue 解耦，" 
          "并通过 await 自动协调快慢（低速不会拖垮高速）。")


if __name__ == "__main__":
    asyncio.run(main())