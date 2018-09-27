import logging

from flask import current_app, session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db

app = create_app("development")

# 创建flask-script对象
manager = Manager(app)

# 将app和db数据库对象进行关联
Migrate(app, db)
# 添加数据库迁移命令到flask-script对象
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    # session["a1"] = "python11111"
    # logging模块中，在终端输出log日志
    logging.debug("这是debug级别的输出")
    logging.info("这是info级别的输出")

    # 在 Flask框架 中，其自己对 Python 的 logging 进行了封装，在 Flask 应用程序中，可以以如下方式进行输出 log
    current_app.logger.debug('debug')
    current_app.logger.error('error')

    return 'index'


if __name__ == '__main__':
    manager.run()
