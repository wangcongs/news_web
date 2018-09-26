from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
    """项目的配置"""
    DEBUG = True
    SECRET_KEY = '8Q63yvFuBbhjXIRQc8H96Yr0LvGXPwmthzalCoQUNto9J9cTD+ChKxb7Yk3RcvzlmIfZvUWPAxPeIg/J/1aV6A=='
    # mysql数据库配置项
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information777"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库配置项
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 指定session的存储位置
    SESSION_TYPE = "redis"
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 指定存储在哪一个redis中
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2


# 初始化app对象
app = Flask(__name__)

# 从对象中加载配置
app.config.from_object(Config)

# 初始化db数据库对象
db = SQLAlchemy(app)
# 创建redis存储对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启当前项目CSRF保护， CSRFProtect只做验证工作，cookie中的 csrf_token 和表单中的 csrf_token 需要我们自己实现
CSRFProtect(app)
# 为app添加session存储位置Session类的作用，就是为为app指定session的存储位置的
Session(app)

# 创建flask-script对象
manager = Manager(app)

# 将app和db数据库对象进行关联
Migrate(app, db)
# 添加数据库迁移命令到flask-script对象
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    session["a1"] = "python11111"
    return 'index'


if __name__ == '__main__':
    manager.run()
