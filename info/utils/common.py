# 用来存放自定义的工具类
import functools

from flask import session, current_app, g

from info.models import User


def do_index_class(index):
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    else:
        return ""


# 定义一个装饰器，用来实现检测用户登录情况
# 使用 functools.wraps 去装饰内层函数，可以保持当前装饰器去装饰的函数的 __name__ 的值不变
def user_login_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # 从session中获取user_id的数值（查询登录状态）
        user_id = session.get("user_id", None)
        # 提前将user模型置为None
        user = None
        # 从数据库中查询user模型
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
        # 将查询到的结果赋给g变量
        g.user = user
        return f(*args, **kwargs)
    return wrapper


# 定义一个函数，在需要进行登录检测的时候，调用此函数就可以（可行）
# def user_login_data():
#         # 从session中获取user_id的数值（查询登录状态）
#         user_id = session.get("user_id", None)
#         # 提前将user模型置为None
#         user = None
#         # 从数据库中查询user模型
#         try:
#             user = User.query.get(user_id)
#         except Exception as e:
#             current_app.logger.error(e)
#         return user
