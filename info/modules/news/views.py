from flask import render_template, request, session, current_app, g, abort

from info import constants
from info.models import User, News
# from info.utils.common import user_login_data
from info.utils.common import user_login_data
from . import news_blu


@news_blu.route("/<int:news_id>")
@user_login_data
def news_detail(news_id):
    """
    显示新闻详情页
    :param news_id:
    :return:
    """

    """
    # 1.查询用户登录情况，如果登录，将右上角信息显示需要数据传给摸板（和首页一样的操作）
    # 从session中获取用户信息,如果获取失败，返回None
    user_id = session.get("user_id", None)
    # 先将user模型对象置为None
    user = None
    if user_id:
        # 从根据获取到的 user_id 数据库查询用户模型
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    # 将用户模型对象转化成字典形式，传给摸板data
"""
    # 调用函数的方式实现登录检验，也可行，但是此处我们使用装饰器的形式
    # user = user_login_data()

    user = g.user

    # 2.从数据库查询排行信息，将数据传给摸板（和首页一样的操作）
    # 定义一个空的列表，防止数据库查询失败，列表不存在
    news_list = list()
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 定义一个空的字典列表
    news_dict_list = list()
    # 遍历模型对象列表，将其以字典的形式存入字典列表（字典包含新闻的各种详细信息）
    for news in news_list:
        news_dict_list.append(news.to_basic_dict())

    # 3.从数据库查询出当前news_id新闻内容，显示在新闻详情页中
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    # 如果未查到请求的新闻，抛出404错误,后面会统一处理404错误
    if not news:
        abort(404)
    # 新闻点击点击此处+1
    news.clicks += 1
    # 先设置一个布尔值，表示新闻是否被收藏
    is_collected = False

    if user:
        # 此处查询所有的新闻不需要加all()，动态显示的模式会让在需要使用时，自动加载
        if news in user.collection_news:
            is_collected = True

    # 将得到的数据存储起来
    data = {
        "user_info": user.to_dict() if user else None,
        "news_dict_list": news_dict_list,
        "news": news.to_dict(),
        "is_collected": is_collected
    }
    return render_template("news/detail.html", data=data)
