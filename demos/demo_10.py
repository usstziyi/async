def gen():
    yield 1
    yield 2
    return "done"

g = gen()
print(next(g))  # 1
print(next(g))  # 2


try:
    next(g)
except StopIteration as e:
    print(e.value)  # "done" —— 这就是 return 的值
