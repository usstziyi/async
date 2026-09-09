import asyncio

"""
anext() 是 Python 内置函数（built-in），就像 next()、len()、print() 一样，属于内置作用域，不需要 import。
"""

async def hello_steps():
    print("步骤1开始执行")
    await asyncio.sleep(1)
    yield "步骤1完成：中间结果A"
    
    print("步骤2开始执行")
    await asyncio.sleep(1)
    yield "步骤2完成：中间结果B"

async def main():
    agen = hello_steps()
    
    # 使用 anext() 函数，带默认值
    result1 = await anext(agen, "默认结束")
    print(f"收到中间结果：{result1}")
    
    result2 = await anext(agen, "默认结束")
    print(f"收到中间结果：{result2}")
    
    # 第三次调用会返回默认值
    result3 = await anext(agen, "默认结束")
    print(f"收到中间结果：{result3}")
    
    await agen.aclose()

asyncio.run(main())