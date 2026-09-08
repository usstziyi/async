"""demo_01：同步基线 —— 感受"阻塞"的本质

目标：搞清楚"程序为什么会卡住"，这是理解 async 的前提。

下面的 cook() 用 sleep 模拟一个真实的耗时操作（比如请求网络、读数据库、读文件）。
同步代码里，程序一行一行往下走，遇到 sleep 就必须干等，等完才走下一行。
"""
import time


def cook(name: str, seconds: float) -> str:
    """同步函数：模拟"做一道菜"，耗时 seconds 秒，期间什么事情都干不了。"""
    print(f"    开始做 [{name}]，预计 {seconds}s，先把锅占住...")
    time.sleep(seconds)  # 同步阻塞：线程在这里干等，没法做其它事
    return f"    [{name}] 做好了！"

def main():
    print("===== 同步做三宫格 3 道菜，串行执行 =====")
    # 记录程序开始执行的精确时间，用于计算后续总耗时
    start = time.perf_counter()

    # 必须一个一个来：前一个 sleep 完，才轮到下一个
    r1 = cook("西红柿", 1.0)
    r2 = cook("土豆", 2.0)
    r3 = cook("牛肉", 3.0)

    elapsed = time.perf_counter() - start
    print("\n结果：")
    print(r1); print(r2); print(r3)
    print(f"\n总耗时：{elapsed:.2f}s （= 1 + 2 + 3，纯串行累加）\n")
    print("核心理解：同步代码里 sleep 是'死等'，CPU 明明空闲却不去干别的。")


if __name__ == "__main__":
    main()