function get_job_list(page, limit) {
    var job_class = $("#job_class").val();
    $.get('/api/job/', {option: 'all', job_class: job_class, page: page, limit: limit}, function (ret) {
        if (!ret.error_code) {
            var data = ret.data;
            var page_num = ret.page_num;
            var job_data = [];
            for (i in data) {
                var job = data[i];
                job_data.push(
                    {
                        name: '<a href=/dashboard/job_detail/?job_id=' + job.id + '>' + job.name + '</a></td>',
                        department: job.department,
                        location: job.location,
                        classes: job.classes,
                        time: job.time,
                        button: '<a target="_blank" class="btn btn-primary btn-xs" href=/dashboard/edit_job/?job_id=' + job.id + '>' + '编辑' + '</a>'
                    }
                );

            }
            $('#table').bootstrapTable('load', job_data);
            if (data.length == 0) {
                $('#pagination-demo').twbsPagination('destroy');
                $('#pagination-demo').twbsPagination({
                    totalPages: 1,
                    visiblePages: 7,
                    first: '首页',
                    prev: '上一页',
                    next: '下一页',
                    last: '末页'
                    //onPageClick: function (event, page) {
                    //    get_job_list(page, 30)
                    //}
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
                    //onPageClick: function (event, page) {
                    //    get_job_list(page, 30)
                    //}
                }).on('page', function (evt, page) {
                    get_job_list(page, 30)
                });

            }
            ;
        }
        ;

    });
}
//
//
function init() {
    $('#table').bootstrapTable({
        columns: [
            {
                field: 'name',
                title: '名称'
            },
            {
                field: 'department',
                title: '部门'
            },
            {
                field: 'location',
                title: '位置'
            },
            {
                field: 'classes',
                title: '类型'
            },
            {
                field: 'time',
                title: '发布时间'
            },
            {
                field: 'button',
                title: '操作'
            }
        ]
    });
    get_job_list(1, 30);


}

init();
