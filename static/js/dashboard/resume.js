$("#pass").click(function () {
    var box_id = GetQueryString('box_id');


    $.post('/api/box/', {option: 'update', box_id: box_id, drop_state: 300}, function (ret) {
        if (!ret.error_code) {
            window.location.href = '/dashboard/resume_detail/?box_id=' + ret.id;
        } else {
            alert(ret.msg)
        }
    })
});

$("#reject").click(function () {
    var box_id = GetQueryString('box_id');
    $.post('/api/box/', {option: 'update', box_id: box_id, drop_state: 200}, function (ret) {
        if (!ret.error_code) {
            window.location.href = '/dashboard/resume_detail/?box_id=' + ret.id;
        } else {
            alert(ret.msg)
        }
    })

});


function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return unescape(r[2]);
    return null
}