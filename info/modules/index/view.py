from flask import render_template, current_app

from . import index_blu
# from info import redis_store


@index_blu.route("/")
def index():
    # 在redis设置一个数据，name : wangwu
    # redis_store.set("name", "wangwu")
    # render_template 会从app创建文件所在的同级templates下找静态文件
    return render_template("news/index.html")


# 访问网站时，浏览器会自动请求根路径 + favicon.ico ，将请求到的文件作为标签的图标,如果不设置就会返回404
# INFO:werkzeug:127.0.0.1 - - [28/Sep/2018 19:45:19] "GET /favicon.ico HTTP/1.1" 200 -
# send_static_file 时flask内置的，去查找指定静态文件时，所调用的方法
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")
