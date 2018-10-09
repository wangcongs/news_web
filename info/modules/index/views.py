from flask import render_template, current_app, session, request, jsonify

from info import constants
from info.models import User, News, Category
from info.utils.response_code import RET
from . import index_blu
# from info import redis_store


# 页面加载完成后，由前端发起一次异步的请求，请求本视图函数的数据
@index_blu.route("/news_list")
def news_list():
    """
    获取首页新闻数据
    :return:
    """
    # 由于获取新闻数据是get请求，使用如下方式获得相关接口参数
    cid = request.args.get('cid', "1")
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)

    # 校验参数
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 根据接收到的参数，在数据库中查询数据
    filters = list()  # 默认查询条件是一个空的列表
    if cid != 1:  # 查询的不是最新数据，而是分类中中的数据（cid=1是【最新】的分类）,就将查询条件添加进去
        filters.append(News.category_id == cid)

    # 查询数据
    try:
        # 得到一个模型分页查询的对象
        paginates = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询错误")

    # 获取当前页的数据
    current_page = paginates.page  # 当前页数
    total_page = paginates.pages  # 总页数
    news_model_list = paginates.items  # 当前页新闻模型对象列表

    news_dict_list = list()
    for news in news_model_list:
        news_dict_list.append(news.to_basic_dict())

    # 将数据装换成字典对象形式，返回
    data = {
        "current_page": current_page,
        "total_page": total_page,
        "cid": cid,
        "news_dict_list": news_dict_list
    }

    return jsonify(errno=RET.OK, errmsg="OK", data=data)


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

    # 从数据库查询出分类信息
    categories = list()
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    # 将获得的模型对象列表转化成字典
    categories_dice_list = list()
    for category in categories:
        categories_dice_list.append(category.to_dict())

    # 将数据 添加到对象中
    data = {
        "user_info": user.to_dict() if user else None,
        "news_dict_list": news_dict_list,
        "categories_dice_list": categories_dice_list
    }
    return render_template("news/index.html", data=data)


# 访问网站时，浏览器会自动请求根路径 + favicon.ico ，将请求到的文件作为标签的图标,如果不设置就会返回404
# INFO:werkzeug:127.0.0.1 - - [28/Sep/2018 19:45:19] "GET /favicon.ico HTTP/1.1" 200 -
# send_static_file 时flask内置的，去查找指定静态文件时，所调用的方法
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")
