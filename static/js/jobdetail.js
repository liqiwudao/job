$("#submit").click(function () {
    var job_id = $(this).attr("job_id");
    $.post("/api/box/", {job_id: job_id}, function (ret) {
        if (!ret.error_code) {
            window.location.href = '/user/drop_box/';

        } else {
            if (ret.error_code == 4004) {
                var flag = confirm(ret.msg);
                if (flag) {
                    window.open('/resume_check/');
                }
                return false
            }
            alert(ret.msg);
            return false

        }
        ;
    });
});
