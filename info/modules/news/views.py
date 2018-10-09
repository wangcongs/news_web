from flask import render_template, request, session, current_app

from info import constants
from info.models import User, News
from . import news_blu


@news_blu.route("/<int:news_id>")
def news_detail(news_id):
    """
    显示新闻详情页
    :param news_id:
    :return:
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

    data = {
        "user_info": user.to_dict() if user else None,
        "news_dict_list": news_dict_list
    }
    return render_template("news/detail.html", data=data)
