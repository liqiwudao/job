function get_box_list(page, limit, drop_state) {

    $.get('/api/box/', {
        page: page, limit: limit, drop_state: drop_state
    }, function (ret) {
        if (!ret.error_code) {
            var data = ret.data;
            $("#body").html('');
            for (i in data) {
                var job = data[i];
                if (job.drop_state == 100) {
                    var drop_state = '<p class="drop-success pt-10">投递成功</p>'
                } else if (job.drop_state == 200) {
                    var drop_state = '<p class="drop-wait pt-10">待面试</p>'

                } else if (job.drop_state == 300) {
                    var drop_state = '<p class="drop-fail pt-10">不合适</p>'
                }

                $("#body").append(
                    '<div class="single-job-post fix">' +
                    '<div class="job-title col-4 pl-30">' +
                    '<div class="fix pl-30 mt-29">' +
                    '<h4 class=" mb-5">' +
                    '<span class="job-btn" job_id=' + job.id + '>' + job.name + '</span>' +
                    '<span class="ml-10 job-time">' + job.time + '</span>' +
                    '</h4>' +
                    '<div class="pt-5">' +
                    '<span class="job-salary">' + job.salary + '</span>' +
                    '<span class="ml-10">经验</span><span>' + job.experience + '</span>' +
                    '<span>/</span>' +
                    '<span>' + job.education + '</span>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '<div class="address col-4 pl-50">' +
                    '<span class="mtb-30 block">工作地点<br>' + job.location + '</span>' +
                    '</div>' +
                    '<div class=" col-2 text-center pt-24">' +
                    '<h4>' + job.department + '</h4>' +
                    '<div class="pt-10">' +
                    '<span>' + job.temptation + '</span>' +
                    drop_state +
                    '</div>' +
                    '</div>' +
                    '</div>'
                );

                $(".job-btn").click(function () {
                    var job_id = $(this).attr('job_id');
                    window.open('/job/?job_id=' + job_id);
                });


            }

            if (data.length == 0) {
                $("#body").html('<p class="text-center">未找到符合条件的内容</p>');

            }
        }
        ;

    });
}
//
function init() {
    $('.drop-tab a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var drop_state = $(this).attr("name");
        get_box_list(1, 10, drop_state);
    });

    get_box_list(1, 10, 0);

}

init();

