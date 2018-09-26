
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import app, db

# 创建flask-script对象
manager = Manager(app)

# 将app和db数据库对象进行关联
Migrate(app, db)
# 添加数据库迁移命令到flask-script对象
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    # session["a1"] = "python11111"
    return 'index'


if __name__ == '__main__':
    manager.run()
