# 存放新闻详情相关的内容
# 创建蓝图对象
from flask import Blueprint

news_blu = Blueprint("news", __name__, url_prefix="/news")

from .views import *
