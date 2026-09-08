"""demo_02：async/await 入门与事件循环

目标：引入 asyncio。认识两个关键词：
  - async def   ：定义"协程"（coroutine），一个可以被挂起/恢复的函数
  - await        ：在协程里"让出控制权"，等待另一个协程完成

关键点：
  - 协程对象不是一调用就跑，必须交给事件循环去调度。
  - await 只是"让出"，如果还是一个个 await 串行，并发度并不会提升
    —— 这正好引出 demo_03 的并发工具。
"""
import asyncio


async def cook(name: str, seconds: float, tag: str) -> str:
    """async 版本的 cook。await asyncio.sleep() 会"挂起"当前协程，让事件循环去跑别人。"""
    print(f"    [{tag}] 开始做 [{name}]，预计 {seconds}s...")
    await asyncio.sleep(seconds)  # 挂起：事件循环可以先去做其它协程
    return f"    [{tag}] [{name}] 做好了！"


async def main():
    print("===== demo_02：最朴素的 async 写法（尚未并发） =====")
    start = asyncio.get_event_loop().time()

    # 这样写：依然串行！await 一个，等完再 await 下一个
    r1 = await cook("西红柿", 1.0, "A")
    r2 = await cook("土豆", 2.0, "B")
    r3 = await cook("牛肉", 3.0, "C")

    elapsed = asyncio.get_event_loop().time() - start
    print("\n结果：")
    print(r1); print(r2); print(r3)
    print(f"\n总耗时：{elapsed:.2f}s")
    print("结论：改成 async 并不会自动变快！原因：A 的 await 挂起后，事件循环并没有被安排去跑 B。")
    print("      真正的并发来自 demo_03：同时启动 / 并派多个协程。")


if __name__ == "__main__":
    asyncio.run(main())  # asyncio.run 是启动事件循环的入口