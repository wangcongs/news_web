from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    """项目的配置"""
    DEBUG = True
    # 链接数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information777"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 初始化app对象
app = Flask(__name__)

# 从对象中加载配置
app.config.from_object(Config)

# 初始化db数据库对象
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
