from . import index_blu
from info import redis_store


@index_blu.route("/")
def index():
    # 在redis设置一个数据，name : wangwu
    redis_store.set("name", "wangwu")
    return 'index'
