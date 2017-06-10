var wait = 60;
function init() {
    $("#get_code").addClass("disabled");
    time()
}
function time() {
    if (wait == 0) {
        $("#get_code").removeClass("disabled");
        $("#get_code").text("获取验证码");
        wait = 59
    } else {
        $("#get_code").text(wait + "s重新发送");
        wait--;
        setTimeout(function () {
            time()
        }, 1000)
    }
}

$("#get_code").click(function () {
    if ($("#get_code").hasClass("disabled")) {
        return false
    }
    var tel = $("#tel").val();
    if (!tel) {
        $("#tel").popover({trigger: "manual", content: "请输入手机号", placement: "top"});
        $("#tel").popover("show");
        setTimeout(function () {
            $('#tel').popover('destroy')
        }, 1500);
        return false
    } else {
        if (!/1[3|4|5|7|8]\d{9}/.test(tel)) {
            $("#tel").popover({trigger: "manual", content: "手机号输入错误，请重新输入", placement: "top"});
            $("#tel").popover("show");
            setTimeout(function () {
                $('#tel').popover('destroy')
            }, 1500);
            return false
        }
    }
    $.post("/api/check_code_admin/", {tel: tel}, function (msg) {
        if (msg.error_code) {
            $("#tel").popover({trigger: "manual", content: msg.msg, placement: "top"});
            $("#tel").popover("show");
            setTimeout(function () {
                $('#tel').popover('destroy')
            }, 1500);
            return false
        }
        init();
    })
});


$("#submit").click(function () {
    var tel = $("#tel").val();
    var code = $("#code").val();


    if (!tel) {
        $("#tel").popover({trigger: "manual", content: "请输入手机号", placement: "top"});
        $("#tel").popover("show");
        setTimeout(function () {
            $('#tel').popover('destroy')
        }, 1500);
        return false

    } else {
        if (!/1[3|4|5|7|8]\d{9}/.test(tel)) {
            $("#tel").popover({trigger: "manual", content: "手机号输入错误，请重新输入", placement: "top"});
            $("#tel").popover("show");
            setTimeout(function () {
                $('#tel').popover('destroy')
            }, 1500);
            return false
        }
    }
    if (!code) {
        $("#code").popover({trigger: "manual", content: "请输入验证码", placement: "top"});
        $("#code").popover("show");
        setTimeout(function () {
            $('#code').popover('destroy')
        }, 1500);
        return false
    } else {
        if (code.length != 6) {
            $("#code").popover({trigger: "manual", content: "请输入6位验证码", placement: "top"});
            $("#code").popover("show");
            setTimeout(function () {
                $('#code').popover('destroy')
            }, 1500)
        }
    }
    //if (!passwd) {
    //    $("#password").popover({trigger: "manual", content: "请输入登入密码", placement: "top"});
    //    $("#password").popover("show");
    //    setTimeout(function () {
    //        $('#password').popover('destroy')
    //    }, 1500);
    //    return false
    //} else {
    //    if (passwd.length < 6) {
    //        $("#password").popover({trigger: "manual", content: "登入密码必须在6位以上", placement: "top"});
    //        $("#password").popover("show");
    //        setTimeout(function () {
    //            $('#password').popover('destroy')
    //        }, 1500);
    //        return false
    //    }
    //}
    $.post("/api/admin_login/", {tel: tel, recv_code: code}, function (msg) {
        if (!msg.error_code) {
            var url = GetQueryString('redirect');
            if (!url) {
                window.location.href = "/dashboard/";
            } else {
                window.location.href = url;
            }
        } else {
            $("#code").popover({trigger: "manual", content: "验证码错误", placement: "top"});
            $("#code").popover("show");
            setTimeout(function () {
                $('#code').popover('destroy')
            }, 1500)
        }
    })
});


function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return unescape(r[2]);
    return null
}

