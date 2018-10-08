from redis import StrictRedis
import logging


class Config(object):
    """项目的配置"""
    SECRET_KEY = '8Q63yvFuBbhjXIRQc8H96Yr0LvGXPwmthzalCoQUNto9J9cTD+ChKxb7Yk3RcvzlmIfZvUWPAxPeIg/J/1aV6A=='
    # mysql数据库配置项
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information777"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 对SQLAlchemy对象进行如下配置，则在视图函数中对模型对象属性进行修改的时候，不在需要手动commite，在请求结束的时候，会自动执行一次db.session.commite()的操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

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

    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """开发环境下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境下的配置"""
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class TestingConfig(Config):
    """测试环境下的配置"""
    DEBUG = True
    TESTING = True


# 定义一个字典，存储各种环境下的配置类信息
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
