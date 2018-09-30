from flask import request, abort, current_app, make_response

from info import redis_store, constants
from . import passport_blu

from info.utils.captcha.captcha import captcha


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
