"""
应用场景
✅ API 调用次数限制
✅ 防止暴力破解（密码尝试限制）
✅ 资源访问控制
✅ 测试环境中的函数调用监控
关键记忆点：
用闭包保存状态（call_count）
用 nonlocal 修改外部变量
用 @functools.wraps 保留元信息
返回 None 或抛出异常来阻止执行
"""


# import functools
#
#
# def limit_calls(max_times=3):
#     """
#     装饰器：限制函数最多被调用 max_times 次
#     :param max_times: 最大调用次数，默认为3
#     """
#     def decorator(func):
#         call_count = 0  # 记录调用次数
#
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             nonlocal call_count
#
#             if call_count >= max_times:
#                 print("已达上限")
#                 return None
#
#             call_count += 1
#             print(f"第 {call_count} 次调用")
#             return func(*args, **kwargs)
#
#         # 添加查看剩余次数的功能
#         wrapper.remaining_calls = lambda: max_times - call_count
#         wrapper.reset = lambda: setattr(wrapper, '_reset', call_count := 0)
#
#         return wrapper
#     return decorator
#
#
# # ===== 测试代码 =====
# @limit_calls(3)
# def say_hello(name):
#     """打招呼函数"""
#     return f"Hello, {name}!"
#
#
# @limit_calls(3)
# def add(a, b):
#     """加法函数"""
#     return a + b
#
#
# if __name__ == "__main__":
#     print("=" * 40)
#     print("测试 say_hello 函数:")
#     print("=" * 40)
#
#     # 前3次调用成功
#     print(say_hello("张三"))   # 第 1 次调用, Hello, 张三!
#     print(say_hello("李四"))   # 第 2 次调用, Hello, 李四!
#     print(say_hello("王五"))   # 第 3 次调用, Hello, 王五!
#
#     # 第4次调用被限制
#     print(say_hello("赵六"))   # 已达上限, None
#
#     print("\n" + "=" * 40)
#     print("测试 add 函数:")
#     print("=" * 40)
#
#     print(add(1, 2))           # 第 1 次调用, 3
#     print(add(3, 4))           # 第 2 次调用, 7
#     print(add(5, 6))           # 第 3 次调用, 11
#     print(add(7, 8))           # 已达上限, None


import functools

def limit_calls(func):
    """装饰器：限制函数最多调用3次"""
    call_count = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count

        if call_count >= 3:
            print("已达上限")
            return None

        call_count += 1
        return func(*args, **kwargs)

    return wrapper


@limit_calls
def test():
    print("执行了")


test()  # 执行了
test()  # 执行了
test()  # 执行了
test()  # 已达上限




# 进阶版本（带重置功能）
# import functools
#
#
# def limit_calls(max_times=3):
#     """装饰器：限制函数调用次数，支持重置"""
#
#     def decorator(func):
#         state = {'count': 0}  # 使用字典避免 nonlocal
#
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             if state['count'] >= max_times:
#                 print("已达上限")
#                 return None
#
#             state['count'] += 1
#             return func(*args, **kwargs)
#
#         def reset():
#             """重置计数器"""
#             state['count'] = 0
#             print("计数器已重置")
#
#         wrapper.reset = reset
#         return wrapper
#
#     return decorator
#
#
# # 使用
# @limit_calls(3)
# def greet(name):
#     return f"Hi, {name}"
#
#
# print(greet("Alice"))  # Hi, Alice
# print(greet("Bob"))  # Hi, Bob
# print(greet("Charlie"))  # Hi, Charlie
# print(greet("David"))  # 已达上限
#
# greet.reset()  # 计数器已重置
# print(greet("Eve"))  # Hi, Eve（又可以调用了）
