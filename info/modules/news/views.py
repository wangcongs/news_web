from flask import render_template, request, session, current_app, g, abort, jsonify

from info import constants, db
from info.models import User, News, Comment
# from info.utils.common import user_login_data
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import news_blu


news_blu.route("/news/news_comment", methods=["POST"])
@user_login_data
def news_comment():
    """
    评论新闻和回复别人评论
    1、接收三个参数
    2、对参数进行校验
    3、新闻是否存在校验
    4、存入评论的数据库
    :return:
    """
    # 先判断用户是否登录
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    # 获取参数
    news_id = request.json.get("news_id", None)
    comment_content = request.json.get("comment", None)
    parent_id = request.json.get("parent_id", None)

    # 校验参数
    if not all([news_id, comment_content]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")
    # 校验新闻id是否正确
    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数格式错误")
    # 查询新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到新闻数据")

    # 初始化一个评论模型，并且赋值
    comment = Comment()
    comment.news_id = news_id
    comment.user_id = user.id
    comment.content = comment_content
    if parent_id:
        comment.parent_id = parent_id

    # 提交到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据提交错误")

    # 操作成功 回应，并将评论内容返回给前端，用来显示评论
    return jsonify(errno=RET.OK, errmsg="操作成功", comment=comment.to_dict())






@news_blu.route('/news_collect', methods=["POST"])
@user_login_data
def news_collect():
    """
    收藏新闻(取消收藏逻辑和收藏逻辑类似，也使用这个视图函数，只需要传递过来一个action就可以)
    1. 接受参数
    2. 判断参数
    3. 查询新闻，并判断新闻是否存在
    :return:
    """

    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    # 1. 接受参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")

    # 2. 判断参数
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if action not in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3. 查询新闻，并判断新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到新闻数据")

    # 4. 收藏以及取消收藏
    if action == "cancel_collect":
        # 取消收藏
        if news in user.collection_news:
            user.collection_news.remove(news)
    else:
        # 收藏
        if news not in user.collection_news:
            # 添加到用户的新闻收藏列表
            user.collection_news.append(news)

    return jsonify(errno=RET.OK, errmsg="操作成功")


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
