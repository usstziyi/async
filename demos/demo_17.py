import asyncio

async def hello_steps():
    print("步骤1开始执行")
    await asyncio.sleep(1)
    yield "步骤1完成：中间结果A"  # 产出第1个业务结果
    
    print("步骤2开始执行")
    await asyncio.sleep(1)
    yield "步骤2完成：中间结果B"  # 产出第2个业务结果
    
    return  # 语法限制：async生成器不能"return 值"，只能用裸return结束迭代（PEP 525）

async def main():
    # 用 async for 遍历所有中间产出
    async for step_result in hello_steps():
        print(f"收到中间结果：{step_result}")

asyncio.run(main())
