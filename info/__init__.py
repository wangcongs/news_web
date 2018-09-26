from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from config import Config


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