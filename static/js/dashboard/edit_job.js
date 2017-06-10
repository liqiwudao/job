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
    var temptation = $("#job_temptation").val();
    var description = $("#editor").cleanHtml();

    if (!job_name) {
        alert("请填写职位名称");
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
        option: 'update',
        job_id: GetQueryString('job_id'),
        job_class: job_class,
        job_name: job_name,
        job_department: job_department,
        job_category: job_category,
        job_experience: job_experience,
        education: education,
        salary_start: salary_start,
        salary_end: salary_end,
        location: location,
        description: description,
        temptation: temptation
    };


    $.post('/api/job/', data, function (ret) {
        if (!ret.error_code) {
            window.location.href = '/dashboard/job_detail/?job_id=' + ret.id;
        } else {
            alert(ret.msg);
            return false;
        }
    });

});


function init_data() {
    var data = $("#data").attr("data");
    var obj = $.parseJSON(data);
    $("#job_class option[value=" + obj.classes + "]").attr("selected", true);
    $("#job_name").val(obj.name);
    $("#job_department").val(obj.department);
    $('#job_category input[value=' + obj.category + ']').attr("checked", true);
    $("#job_experience option[value=" + obj.experience + "]").attr("selected", true);
    $("#education option[value=" + obj.education + "]").attr("selected", true);
    $("#salary_start").val(obj.salary_start);
    $("#salary_end").val(obj.salary_end);
    $("#location").val(obj.location);
    $("#editor").html(obj.description);
    $("#job_temptation").val(obj.temptation)

}

init_data();

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return unescape(r[2]);
    return null
}

