$("#submit").click(function () {
    var job_class = $("#job_class").val();
    var job_name = $("#job_name").val();
    var job_department = $("#job_department").val();
    var job_category = $('#job_category input[name="category"]:checked').val();
    var job_experience = $("#job_experience").val();
    var education = $("#education").val();
    var salary_start = $("#salary_start").val();
    var salary_end = $("#salary_end").val();
    var location = $("#location").val();
    var description = $("#editor").cleanHtml();
    var temptation = $('#job_temptation').val();

    if (!job_name) {
        alert("请填写职位名称");
        return false;
    }
    ;

    if (!temptation) {
        alert("请填写职位诱惑");
        return false;
    }
    ;

    if (!job_department) {
        alert("请填写招聘部门");
        return false;
    }
    ;

    if (!salary_start) {
        alert("请填写薪资范围");
        return false;
    }
    ;

    if (!salary_end) {
        alert("请填写薪资范围");
        return false;
    }
    ;
    if (Number(salary_start) > Number(salary_end)) {
        alert('薪资范围错误');
        return false;
    }

    if (!location) {
        alert("请填写工作地址");
        return false;
    }
    ;

    if (!description) {
        alert("请填写职位描述");
        return false;
    }
    ;

    data = {
        job_class: job_class,
        job_name: job_name,
        job_department: job_department,
        job_category: job_category,
        job_experience: job_experience,
        education: education,
        salary_start: salary_start,
        salary_end: salary_end,
        location: location,
        temptation: temptation,
        description: description
    };


    $.post('/api/job/', data, function (ret) {
        if (!ret.error_code) {
            //alert("ok");
            window.location.href = '/dashboard/job/'
        } else {
            alert(ret.msg);
            return false;
        }
    });

});
