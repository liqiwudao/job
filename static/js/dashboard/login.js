function init_user() {
    $.get('/api/dashboard_user/', {}, function (ret) {
        var user = ret.user;
        if (user) {
            $('#user_name').text(user.name);
        }
    })
}

init_user();


function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return unescape(r[2]);
    return null
}

