import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from config import config
# 在此处导入蓝图对象，会导致循环导入的问题，应该将蓝图在注册时再导入
# from info.modules.index import index_blu

# 初始化数据库
db = SQLAlchemy()
# 将redis存储对象定义成一个全局变量，并使用python3.6的新特性，利用注释指明变量的类型
redis_store = None  # type:StrictRedis


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 调用配置日志的函数
    setup_log(config_name)
    # 初始化app对象
    app = Flask(__name__)

    # 从对象中加载配置
    app.config.from_object(config[config_name])

    # 初始化db数据库对象
    # db = SQLAlchemy(app)
    # flask中很多扩展里面都可以先初始化扩展对象，然后再调用对象的init_app方法进行初始化
    db.init_app(app)
    # 创建redis存储对象
    global redis_store  # 作为修改全局变量
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT, decode_responses=True)
    # 开启当前项目CSRF保护， CSRFProtect只做验证工作，cookie中的 csrf_token 和表单中的 csrf_token 需要我们自己实现
    # CSRFProtect(app)
    # 为app添加session存储位置Session类的作用，就是为为app指定session的存储位置的
    Session(app)

    # 将蓝图注册到app中
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)
    return app
