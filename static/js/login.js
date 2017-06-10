/**
 * Created by apple on 17/2/1.
 */
//
function init_user() {
    var data = $("#user_msg").attr("msg");
    var msg = $.parseJSON(data);
    if (msg.name) {
        if (msg.error_code) {
            return
        } else {
            $('.login').addClass('hidden');
            $('.user').removeClass('hidden');
            $('.user .name').text(msg.name);
            //$(".user .caret").removeClass('hidden');
            $(".resume").attr('href', '/resume_check/');
            $(".drop_box").attr('href', '/user/drop_box/');
            $(".login_out").click(function () {
                $.post('/api/login_out/', {}, function (msg) {
                    if (msg.error_code) {
                        return false
                    } else {
                        //$(".user .caret").addClass('hidden');
                        $('.user').addClass('hidden');
                        $('.login').removeClass('hidden')
                    }
                })
            })
        }
    } else {
        $("#user_msg").attr("msg", '')
    }
}

init_user();

$("#submit").click(function () {
    var tel = $("#l_tel").val();
    var passwd = $("#passwd").val();
    if (!tel) {
        $("#l_tel").popover({trigger: "manual", content: "请输入手机号", placement: "top"});
        $("#l_tel").popover("show");
        setTimeout(function () {
            $('#l_tel').popover('destroy')
        }, 1500);
        return false
    } else {
        if (!/1[3|4|5|7|8]\d{9}/.test(tel)) {
            $("#l_tel").popover({trigger: "manual", content: "手机号输入错误，请重新输入", placement: "top"});
            $("#l_tel").popover("show");
            setTimeout(function () {
                $('#l_tel').popover('destroy')
            }, 1500);
            return false
        }
    }
    if (!passwd) {
        $("#passwd").popover({trigger: "manual", content: "请输入登入密码", placement: "top"});
        $("#passwd").popover("show");
        setTimeout(function () {
            $('#passwd').popover('destroy')
        }, 1500);
        return false
    } else {
        if (passwd.length < 6) {
            $("#passwd").popover({trigger: "manual", content: "登入密码必须在6位以上", placement: "top"});
            $("#passwd").popover("show");
            setTimeout(function () {
                $('#passwd').popover('destroy')
            }, 1500);
            return false
        }
    }
    $.post("/api/login/", {passwd: passwd, tel: tel}, function (msg) {
        if (msg.error_code) {
            if (msg.error_code == "4001") {
                $("#passwd").popover({trigger: "manual", content: msg.msg, placement: "top"});
                $("#passwd").popover("show");
                setTimeout(function () {
                    $('#l_password').popover('destroy')
                }, 1500);
                return false
            }
            if (msg.error_code == "4002") {
                $("#l_tel").popover({trigger: "manual", content: msg.msg, placement: "top"});
                $("#l_tel").popover("show");
                setTimeout(function () {
                    $('#l_tel').popover('destroy')
                }, 1500);
                return false
            }
        } else {
            var url = GetQueryString('redirect');
            if (!url) {
                window.location.href = "/"
            } else {
                window.location.href = url
            }
        }
    })
});


function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return unescape(r[2]);
    return null
}
