from . import index_blu


@index_blu.route("/")
def index():
    # session["a1"] = "python11111"
    # logging模块中，在终端输出log日志
    # logging.debug("这是debug级别的输出")
    # logging.info("这是info级别的输出")

    # 在 Flask框架 中，其自己对 Python 的 logging 进行了封装，在 Flask 应用程序中，可以以如下方式进行输出 log
    # current_app.logger.debug('debug')
    # current_app.logger.error('error')
    return 'index'
