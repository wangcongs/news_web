$(function(){

	// 打开登录框
	$('.login_btn').click(function(){
        $('.login_form_con').show();
	})
	
	// 点击关闭按钮关闭登录框或者注册框
	$('.shutoff').click(function(){
		$(this).closest('form').hide();
	})

    // 隐藏错误
    $(".login_form #mobile").focus(function(){
        $("#login-mobile-err").hide();
    });
    $(".login_form #password").focus(function(){
        $("#login-password-err").hide();
    });

    $(".register_form #mobile").focus(function(){
        $("#register-mobile-err").hide();
    });
    $(".register_form #imagecode").focus(function(){
        $("#register-image-code-err").hide();
    });
    $(".register_form #smscode").focus(function(){
        $("#register-sms-code-err").hide();
    });
    $(".register_form #password").focus(function(){
        $("#register-password-err").hide();
    });


	// 点击输入框，提示文字上移
	// $('.form_group').on('click focusin',function(){
	// 	$(this).children('.input_tip').animate({'top':-5,'font-size':12},'fast').siblings('input').focus().parent().addClass('hotline');
	// })
    $('.form_group').on('click',function(){
    $(this).children('input').focus()
    })

    $('.form_group input').on('focusin',function(){
    $(this).siblings('.input_tip').animate({'top':-5,'font-size':12},'fast')
    $(this).parent().addClass('hotline');
    })

	// 输入框失去焦点，如果输入框为空，则提示文字下移
	$('.form_group input').on('blur focusout',function(){
		$(this).parent().removeClass('hotline');
		var val = $(this).val();
		if(val=='')
		{
			$(this).siblings('.input_tip').animate({'top':22,'font-size':14},'fast');
		}
	})


	// 打开注册框
	$('.register_btn').click(function(){
		$('.register_form_con').show();
		generateImageCode()
	})


	// 登录框和注册框切换
	$('.to_register').click(function(){
		$('.login_form_con').hide();
		$('.register_form_con').show();
        generateImageCode()
	})

	// 登录框和注册框切换
	$('.to_login').click(function(){
		$('.login_form_con').show();
		$('.register_form_con').hide();
	})

	// 根据地址栏的hash值来显示用户中心对应的菜单
	var sHash = window.location.hash;
	if(sHash!=''){
		var sId = sHash.substring(1);
		var oNow = $('.'+sId);		
		var iNowIndex = oNow.index();
		$('.option_list li').eq(iNowIndex).addClass('active').siblings().removeClass('active');
		oNow.show().siblings().hide();
	}

	// 用户中心菜单切换
	var $li = $('.option_list li');
	var $frame = $('#main_frame');

	$li.click(function(){
		if($(this).index()==5){
			$('#main_frame').css({'height':900});
		}
		else{
			$('#main_frame').css({'height':660});
		}
		$(this).addClass('active').siblings().removeClass('active');
		$(this).find('a')[0].click()
	})

    // TODO 登录表单提交
    $(".login_form_con").submit(function (e) {
        // 阻止默认行为
        e.preventDefault()
        var mobile = $(".login_form #mobile").val()
        var password = $(".login_form #password").val()

        if (!mobile) {
            $("#login-mobile-err").show();
            return;
        }

        if (!password) {
            $("#login-password-err").show();
            return;
        }

        // 发起登录请求
        params = {
            "mobile": mobile,
            "password": password
        }
        $.ajax({
            url: "/passport/login",
            type: "POST",
            data: JSON.stringify(params),
            contentType: "application/json",
            success:function (resp) {
                if (resp.errno == "0"){
                    // 代表登录成功
                    location.reload()
                } else {
                    // 代表登录失败
                    $("#register-password-err").html(resp.errmsg);
                    $("#register-password-err").show();
                }
            }
        })
    })


    // TODO 注册按钮点击
    $(".register_form_con").submit(function (e) {
        // 阻止默认提交操作
        e.preventDefault()

		// 取到用户输入的内容
        var mobile = $("#register_mobile").val()
        var smscode = $("#smscode").val()
        var password = $("#register_password").val()

		if (!mobile) {
            $("#register-mobile-err").show();
            return;
        }
        if (!smscode) {
            $("#register-sms-code-err").show();
            return;
        }
        if (!password) {
            $("#register-password-err").html("请填写密码!");
            $("#register-password-err").show();
            return;
        }

		if (password.length < 6) {
            $("#register-password-err").html("密码长度不能少于6位");
            $("#register-password-err").show();
            return;
        }

        // 发起注册请求
        var params = {
            "mobile": mobile,
            "smscode": smscode,
            "password": password
        }
        $.ajax({
            url: "/passport/register",
            type: "POST",
            data: JSON.stringify(params),
            contentType: "application/json",
            success: function (resp) {
                if (resp.errno == "0"){
                    // 刷新当前界面
                    location.reload()
                } else {
                    $("#register-password-err").html(resp.errmsg)
                    $("#register-password-err").show()
                }
            }
        })
    })
})

var imageCodeId = ""

// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // 此函数在打开注册框和点击图片时都会被调用
    // 1、生成一个uuid码
    imageCodeId = generateUUID()
    // 2、浏览器向服务器发起一个图片请求,get请求，将获得的uuid发给服务器
    // “/image_code?imageCodeId=imageCodeId”
    var url = "/passport/image_code?imageCodeId=" + imageCodeId
    //3、给img标签设置src属性
    $(".get_pic_code").attr("src", url)

}

// 发送短信验证码
function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".get_code").removeAttr("onclick");
    var mobile = $("#register_mobile").val();
    if (!mobile) {
        $("#register-mobile-err").html("请填写正确的手机号！");
        $("#register-mobile-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err").html("请填写验证码！");
        $("#image-code-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }

    // 发送短信验证码
    var params = {
        "mobile": mobile,
        "image_code": imageCode,
        "image_code_id": imageCodeId
    }
    // 由于是局部刷新，不使用表单请求，表单请求无法控制表单的界面
    $.ajax({
        // 请求地址
        url: "/passport/sms_code",
        // 请求方式
        type: "POST",
        // 请求数据,将字典（js中叫对象），转换成json数据形式
        data: JSON.stringify(params),
        // 请求的数据类型
        contentType: "application/json",
        // 请求成功发出后执行的函数
        success: function (resp) {
            if (resp.errno == "0"){
                // 短信发送成功
                var num = 60;
                // 设置一个定时器
                var t = setInterval(function () {
                    if (num == 1){
                        // 倒计时结束
                        // 清除倒计时
                        clearInterval(t)
                        // 重新设置要显示的内容
                        $(".get_code").html("点击获取验证码");
                        // 重新添加点击事件
                        $(".get_code").attr("onclick", "sendSMSCode();");
                    }else {
                        // 倒计时进行中
                        num -= 1;
                        // 设置a便签显示内容
                        $(".get_code").html(num + "秒后重新获取");
                    }
                }, 1000)

            } else {
                // 表示后端出现了错误，可以将错误信息展示到前端页面中
                $("#register-sms-code-err").html(resp.errmsg);
                $("#register-sms-code-err").show();
                // 将点击按钮的onclick事件函数恢复回去
                $(".get_code").attr("onclick", "sendSMSCode();");
                // 如果错误码是4004，代表验证码错误，重新生成验证码
                if (resp.errno == "4004") {
                    generateImageCode()
                }
            }
        }
    })
}

// 调用该函数模拟点击左侧按钮
function fnChangeMenu(n) {
    var $li = $('.option_list li');
    if (n >= 0) {
        $li.eq(n).addClass('active').siblings().removeClass('active');
        // 执行 a 标签的点击事件
        $li.eq(n).find('a')[0].click()
    }
}

// 一般页面的iframe的高度是660
// 新闻发布页面iframe的高度是900
function fnSetIframeHeight(num){
	var $frame = $('#main_frame');
	$frame.css({'height':num});
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
