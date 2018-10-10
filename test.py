# 深入理解functools工具的使用
import functools


# 使用装饰器@functools.wraps(f)，是为了使被@func装饰的函数的__name__属性值不变
# 如果不使用@functools.wraps(f),则所有被@func装饰过的函数的__name__属性值都变成wrapper了
def func(f):
    @functools.wraps(f)
    def wrapper():
        return f()
    return wrapper


@func
def test1():
    pass


if __name__ == '__main__':
    print(test1.__name__)
