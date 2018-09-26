from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis


class Config(object):
    """项目的配置"""
    DEBUG = True
    # mysql数据库配置项
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information777"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库配置项
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


# 初始化app对象
app = Flask(__name__)

# 从对象中加载配置
app.config.from_object(Config)

# 初始化db数据库对象
db = SQLAlchemy(app)
# 创建redis存储对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启当前项目CSRF保护， 只做服务器验证
CSRFProtect(app)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
