from flask import render_template

from . import index_blu
# from info import redis_store


@index_blu.route("/")
def index():
    # 在redis设置一个数据，name : wangwu
    # redis_store.set("name", "wangwu")
    # render_template 会从app创建文件所在的同级templates下找静态文件
    return render_template("news/index.html")
