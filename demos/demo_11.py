"""
生成器
"""
def my_generator():
    yield 1
    yield 2
    return 3

g = my_generator()  # 返回生成器对象，不执行函数体
print(type(g))  # <class 'generator'>
print(next(g))  # 1
print(next(g))  # 2
try:
    next(g)  # StopIteration
except StopIteration as e:
    print(e.value)  # 有生成器显式 return 时才会有值

print("-----------------")



"""
列表迭代器
"""
# 列表不是迭代器，但可以获取它的迭代器
lst = [3, 2, 1]
it = iter(lst)  # 调用 lst.__iter__()

print(type(it))  # <class 'list_iterator'>
print(next(it))  # 3
print(next(it))  # 2
print(next(it))  # 1

try:
    next(it)  # StopIteration
except StopIteration as e:
    print(e.value)  # StopIteration.value 默认就是 None，只有生成器显式 return 时才会有其他值

print("-----------------")


"""
自定义迭代器
"""
class CountDown:
    def __init__(self, start):
        self.count = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        self.count -= 1
        return self.count + 1

# 使用
cd = CountDown(3)
print(type(cd))  # <class '__main__.CountDown'>
print(next(cd))  # 3
print(next(cd))  # 2
print(next(cd))  # 1


try:
    next(cd) # StopIteration
except StopIteration as e:
    print(e.value)  # None
