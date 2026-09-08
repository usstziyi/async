User asks: besides in front of def methods and before with (async with), where else can "async" appear in Python?

Answer: async keyword can appear:
1. `async def` - define coroutine function / async generator
2. `async with` - async context manager
3. `async for` - iterate async iterable
4. In a `match` statement pattern? Actually `async` is a soft keyword inside match patterns for `as` pattern - `case [x] if ...`. No. Actually in `match` you can use `async` as identifier. Not relevant.

The valid places: `async def`, `async with`, `async for`. In comprehension: `async for` can be used inside list/set/dict comprehensions and generator expressions when inside an async def. E.g. `[x async for x in aiter()]`. Also multiple awaits.

So answer: `async` 只能搭配 def / for / with 三种，出现位置其实是一个声明符。

Explain the grammar:
- async_stmt: "async" (funcdef | with_stmt | for_stmt)
- So `async` only prefixes def, for, with.

Also mention comprehension: inside an async def, you can use `async for` in comprehensions: `[i async for i in agen]`, and `await` in comprehension too `[await f() for f in ...]`.

Give small examples referencing the current demo maybe.

Keep concise Chinese.
`async` 在 Python 里是**只能修饰一种语法**的修饰符。官方语法定义就一句话：

```
async_stmt ::= "async" (funcdef | with_stmt | for_stmt)
```

也就是说，`async` 永远只出现在 **def / for / with** 这三者前面，再没有第四种独立用法。对照这个文件里出现的三种：

**1. `async def` —— 定义协程函数（你已见）**
[第 41 行](file:///d:/AI/trae_code/async/demos/demo_06_async_iter_ctx.py#L41) `async def main():`，整个函数变成一个协程函数，调用它返回协程对象（可被 `await` 或交给 `asyncio.run`）。

**2. `async with` —— 异步上下文管理器（你已见）**
[第 43 行](file:///d:/AI/trae_code/async/demos/demo_06_async_iter_ctx.py#L43) `async with ...`，配合 `__aenter__` / `__aexit__`。

**3. `async for` —— 异步迭代（本文件第 51 行其实也是）**
```python
async for page in page_fetcher(4):
```
遍历异步生成器 / 异步可迭代对象，每次迭代都可能等待。它和第 41、43 行不同，**它不要求"再定义一个 async def"，是放在普通循环的位置**——这是你问的"第三种位置"。

**还有一个变体位置：推导式里可以内嵌 `async for`**
在 `async def` 内部，`async for` 还能直接写进推导式，这是很多人不知道的：

```python
async def main():
    pages = [p async for p in page_fetcher(4)]   # 列表推导式里异步收集
    print(pages)
```

对照记忆表：

| 语法位置 | 作用对象 | 例子 |
|---|---|---|
| `async def` | 协程函数 / 异步生成器 | `async def query()` |
| `async with` | 异步上下文管理器 | `async with DBConnection() as db:` |
| `async for` | 异步可迭代对象 | `async for page in page_fetcher(4):` |
| （推导式中）`async for` | 同上，配合推导式语法 | `[p async for p in agen]` |

所以结论是：`async` **不是修饰变量、不是修饰普通语句**，它只作为这几种"异步语法"的开关。判定方法很简单——只要看到 `async`，后面紧跟的必然是 `def`、`for` 或 `with` 之一。