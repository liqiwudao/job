function get_box_list(page, limit) {
    var drop_state = $("#drop_state").val();
    $.get('/api/box/', {option: 'all', drop_state: drop_state, page: page, limit: limit}, function (ret) {
        if (!ret.error_code) {
            var data = ret.data;
            var page_num = ret.page_num;
            var job_data = [];
            for (i in data) {
                var job = data[i];

                var btn = '';
                if (job.drop_state == 100) {
                    var drop_state = '待审核';

                    var btn = '<a flag=pass class="btn btn-primary btn-xs option-btn" box_id=' + job.box_id + '>' + '通过' + '</a>' + '<a flag=reject class="btn btn-danger btn-xs  option-btn" box_id=' + job.box_id + '>' + '驳回' + '</a>';
                } else if (job.drop_state == 200) {
                    var drop_state = '驳回';
                } else if (job.drop_state == 300) {
                    var drop_state = '通过';

                }
                ;

                job_data.push(
                    {
                        resume_name: '<a href=/dashboard/resume_detail/?box_id=' + job.box_id + '>' + job.resume_name + '</a></td>',
                        tel: job.tel,
                        name: '<a href=/dashboard/job_detail/?job_id=' + job.id + '>' + job.name + '</a></td>',
                        department: job.department,
                        location: job.location,
                        classes: job.classes,
                        time: job.time,
                        button: btn,
                        state: drop_state

                    }
                );

            }
            $('#table').bootstrapTable('load', job_data);


            $(".option-btn").click(function () {
                var flag = $(this).attr("flag");
                var box_id = $(this).attr("box_id");
                if (flag == 'pass') {
                    var drop_state = 300;
                } else if (flag == 'reject') {
                    var drop_state = 200;
                }
                $.post('/api/box/', {option: 'update', box_id: box_id, drop_state: drop_state}, function (ret) {
                    if (!ret.error_code) {
                        get_box_list(1, 30);
                        //window.location.href = '/dashboard/resume_detail/?box_id=' + ret.id
                    } else {
                        alert(ret.msg);
                    }
                });
            });
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
                    get_box_list(page, 30)
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
                    get_box_list(page, 30)
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
                field: 'resume_name',
                title: '姓名'
            },
            {
                field: 'tel',
                title: '电话'
            },

            {
                field: 'department',
                title: '应聘部门'
            },
            {
                field: 'name',
                title: '应聘职位'
            }, {
                field: 'time',
                title: '发布时间'
            },
            {
                field: 'classes',
                title: '类型'
            },

            {
                field: 'state',
                title: '状态'
            },
            {
                field: 'button',
                title: '操作'
            }
        ]
    });
    get_box_list(1, 30);


}

init();
