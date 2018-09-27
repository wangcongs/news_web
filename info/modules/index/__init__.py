from flask import Blueprint

# 创建蓝图对象
index_blu = Blueprint("index_blu", __name__)

from .view import *
