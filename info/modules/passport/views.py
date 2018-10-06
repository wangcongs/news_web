import random
import re

import datetime
from flask import request, abort, current_app, make_response, jsonify, session
from info import redis_store, constants, db
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.utils.response_code import RET
from . import passport_blu
from info.utils.captcha.captcha import captcha


@passport_blu.route("/register", methods=["POST"])
def register():
    """
    注册后端逻辑：
    1、获取手机号，短信验证码，密码三项数据
    2、校验数据是否为空
    3、校验手机号是否正确
    4、校验短信验证码是否正确
    5、校验密码是否符合规则
    6、初始化User数据表模型，将数据存入数据库
    6、返回正确的状态
    :return:
    """
    #   1、获取手机号，短信验证码，密码三项数据
    params_dict = request.json
    mobile = params_dict.get("mobile")
    smscode = params_dict["smscode"]
    password = params_dict["password"]

    #  2、校验数据是否为空
    if not all([mobile, smscode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不能为空")
    # 3、校验手机号是否正确
    if not re.match(r"^1[345678][0-9]{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="电话号码格式输入不正确")

    # 4、校验短信验证码是否正确

    # 从redis中取出短信验证码
    try:
        real_smscode = redis_store.get("mobile_" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询错误")

    # 如果未取到数据
    if not real_smscode:
        return jsonify(errno=RET.NODATA, errmsg="验证码已过期")

    # 校验短信验证码
    if smscode != real_smscode:
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入不正确")

    # 校验密码
    if not re.match(r"[0-9a-zA-Z_]{6,}", password):
        return jsonify(errno=RET.PARAMERR, errmsg="密码至少6位，且为数字字母下划线")

    # 都验证正确之后，初始化User模型，将数据存入数据库
    user = User()
    user.mobile = mobile
    # 暂时没有昵称 ，使用手机号代替
    user.nick_name = mobile
    # 记录最后一次登录的时间
    user.last_login = datetime.datetime.now()
    # 对密码进行处理
    # 模型类中使用propary属性修饰password方法，使得可以像属性一样去访问方法，在赋值时，调用加密程序进行加密
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    # 将数据存储到session中，表明已经登录成功
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nike_name"] = user.nick_name

    # 回应已经响应成功
    return jsonify(errno=RET.OK, errmsg="注册成功")


@passport_blu.route("/sms_code", methods=["POST"])
def send_sms_code():
    """
    发送短信验证码的逻辑：
    1、获取请求的信息（图片验证码信息，验证码ID，手机号）
    2、校验参数（参数是否为空）
    3、根据验证码id 从redis中取出验证码文本
    4、对比验证码是否正确，如果不一致，返回验证码输入有误
    5、验证手机号格式是否输入正确
    6、如果一致，生成一个随机数字（用于验证码使用）
    7、调用短信验证码发送工具，给指定手机号发送验证码
    8、将手机号存入redis中

    :return:
    """
    # 由于传入的参数格式是json
    # 参数实例：'{"mobile": 1888888888, "image_code": "aaaa", "image_code_id": "asdsfagfewr23refw2fs"}'
    # return jsonify(errno=RET.OK, errmsg="短信发送成功")

    # 1、获取参数
    params_dict = request.json
    mobile = params_dict["mobile"]
    image_code = params_dict["image_code"]
    image_code_id = params_dict["image_code_id"]

    # 2、校验参数

    # 所有参数不能为空
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不能为空")

    # 校验电话号码格式是否正确
    if not re.match(r"^1[345678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="电话号码格式输入不正确")

    # 校验验证码是否正确

    # 从redis中取出验证码文本值
    try:
        real_image_code = redis_store.get("imageCodeId_"+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    # 打印一下发现，从数据库中取出的数据是字节形式（b'O5RS'），所以一直对不上，需要设置数据库的时候进行配置，使得取出来的直接是字符串
    print(real_image_code)
    # 校验取到的验证码是否为空
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码已过期")

    # 验证用户输入验证码是否正确
    if image_code.upper() != real_image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")

    # 3、业务逻辑处理
    # 程序走到此处，代表已经验证通过，可以发送验证码

    # 生成一个随机的数字
    sms_code = "%06d" % random.randint(0, 999999)
    # 调用第三方工具发送短信
    result = CCP().send_template_sms(mobile, [sms_code, constants.IMAGE_CODE_REDIS_EXPIRES/60], 1)
    # 判断是否发送成功
    if result != 0:
        return jsonify(errno=RET.THIRDERR, errmsg="短信发送失败")

    # 短信发送成功，将验证码存入数据库
    try:
        redis_store.set("mobile_"+mobile, sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据存储失败")

    # 4、做出响应
    # 验证，且发送成功
    return jsonify(errno=RET.OK, errmsg="短信发送成功")


@passport_blu.route("/image_code")
def get_image_code():
    """
    生成图片，并返回验证码
    1、获取请求参数

    2、判断参数是否为空

    3、若不为空，生成验证码图片

    4、保存图片验证码文本到redis中

    5、返回验证码图片

    :return:
    """
    # 取到参数
    # args 是取到url中 ？ 后面的参数
    image_code_id = request.args.get("imageCodeId", None)
    # 判断参数是否为空
    if not image_code_id:
        return abort(504)
    # 如果取到参数，生成验证码(使用图片验证码工具类)
    name, text, image = captcha.generate_captcha()

    # 将验证码文本存入redis中
    try:
        redis_store.set("imageCodeId_"+image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)
    # 这里直接返回image虽然chrome可以解析曾图片正常显示，但是标识的内容依然是text格式，有些浏览器无法解析
    # 所以不能直接返回image
    # return image

    # 返回图片内容
    response = make_response(image)
    # 设置响应头的响应类型
    response.headers["Content-Type"] = "image/jpg"
    # 返回
    return response
