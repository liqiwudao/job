function get_job_list(page, limit) {
    var job_class = $("#job_class").val();
    var experience = $("#experience").val();
    var category = $("#category").val();

    $.get('/api/job/', {
        job_class: job_class, experience: experience, category: category,
        page: page, limit: limit
    }, function (ret) {
        if (!ret.error_code) {
            var data = ret.data;
            var page_num = ret.page_num;
            $("#body").html('');
            for (i in data) {
                var job = data[i];
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
                $("#body").html('<p class="text-center">未找到符合条件的职位</p>');
                $('#pagination-demo').twbsPagination('destroy');
                $('#pagination-demo').twbsPagination({
                    totalPages: 1,
                    visiblePages: 7,
                    first: '首页',
                    prev: '上一页',
                    next: '下一页',
                    last: '末页'

                }).on('page', function (evt, page) {
                    get_job_list(page, 30)
                });
            } else {
                $('#pagination-demo').twbsPagination('destroy');
                $('#pagination-demo').twbsPagination({
                    totalPages: page_num,
                    visiblePages: 7,
                    first: '首页',
                    prev: '上一页',
                    next: '下一页',
                    last: '末页'

                }).on('page', function (evt, page) {
                    get_job_list(page, 30)
                });

            }
            ;
        }
        ;

    });
}

function init() {
    get_job_list(1, 30);
}

init();

