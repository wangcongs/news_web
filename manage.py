# import logging
# from flask import current_app, session
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


if __name__ == '__main__':
    manager.run()
