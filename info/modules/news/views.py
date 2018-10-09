from flask import render_template
from . import news_blu


@news_blu.route("/<int:news_id>")
def news_detail(news_id):
    """
    显示新闻详情页
    :param news_id:
    :return:
    """
    return render_template("news/detail.html")
