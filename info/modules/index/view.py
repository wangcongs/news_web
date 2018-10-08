from flask import render_template, current_app, session

from info import constants
from info.models import User, News
from . import index_blu
# from info import redis_store


@index_blu.route("/")
def index():
    # 在redis设置一个数据，name : wangwu
    # redis_store.set("name", "wangwu")
    # render_template 会从app创建文件所在的同级templates下找静态文件
    """
    显示首页
    如果用户已经登录，就将登录的信息传递到模板中，供模板使用
    :return:
    """
    # 从session中取到用户ID（用来显示用户的登录信息）
    user_id = session.get("user_id", None)
    user = None
    if user_id:
        # 尝试从数据库中取出当前用户
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 从数据库中查出新闻排行，传递给摸板，进行显示
    news_list = list()
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.looger.error(e)
    # 循环得到的新闻 模型对象列表，得到每一个对象，并将其转化成字典，添加进data中
    # 定义一个存放字典的列表
    news_dict_list = list()
    # 循环得到每一个模型对象
    for news in news_list:
        # 将模型对象转化成字典，添加进字典列表中
        news_dict_list.append(news.to_dict())

    data = {
        "user_info": user.to_dict() if user else None,
        "news_dict_list": news_dict_list
    }
    return render_template("news/index.html", data=data)


# 访问网站时，浏览器会自动请求根路径 + favicon.ico ，将请求到的文件作为标签的图标,如果不设置就会返回404
# INFO:werkzeug:127.0.0.1 - - [28/Sep/2018 19:45:19] "GET /favicon.ico HTTP/1.1" 200 -
# send_static_file 时flask内置的，去查找指定静态文件时，所调用的方法
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")
