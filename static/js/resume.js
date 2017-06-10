function initdate() {

    // Mobiscroll Date & Time initialization
    $('#birthday').mobiscroll().date({
        lang: 'zh', // Specify language like: lang: 'pl' or omit setting to use default
        dateOrder: 'ym',
        dateFormat: 'yy/mm/dd',
        theme: 'mobiscroll',
        display: 'bubble'
    });
    $('#job_date_start').mobiscroll().date({
        lang: 'zh', // Specify language like: lang: 'pl' or omit setting to use default
        dateOrder: 'ym',
        dateFormat: 'yy/mm',
        theme: 'mobiscroll',
        display: 'bubble'
    });
    $('#job_date_end').mobiscroll().date({
        lang: 'zh', // Specify language like: lang: 'pl' or omit setting to use default
        dateOrder: 'ym',
        dateFormat: 'yy/mm',
        theme: 'mobiscroll',
        display: 'bubble'
    });

    $("#graduation_date").mobiscroll().date({
        lang: 'zh', // Specify language like: lang: 'pl' or omit setting to use default
        dateOrder: 'ym',
        dateFormat: 'yy/mm',
        theme: 'mobiscroll',
        display: 'bubble'
    });

};


function init_value() {
    var data = $("#value").attr("data");
    if (data) {
        var ret = $.parseJSON(data);
        $("#name").val(ret.name);
        $("#birthday").val(ret.birthday);
        var sex = Number(ret.sex);
        if (sex == 1) {
            var sex_html = '<label class="uppercase pull-left m-0">性别</label>' +
                '<label class="radio-inline" style="line-height: 44px;">' +
                '<input type="radio" name="sex" id="man" value="1" checked>男' +
                '</label>' +
                '<label class="radio-inline" style="line-height: 44px;">' +
                '<input type="radio" name="sex" id="woman" value="2">女' +
                '</label>'
        } else {

            var sex_html =
                '<label class="uppercase pull-left m-0">性别</label>' +
                '<label class="radio-inline" style="line-height: 44px;">' +
                '<input type="radio" name="sex" id="man" value="1" >男' +
                '</label>' +
                '<label class="radio-inline" style="line-height: 44px;">' +
                '<input type="radio" name="sex" id="woman" value="2" checked>女' +
                '</label>'
        }
        $("#sex").html(sex_html);

        $("#email").val(ret.email);

        $("#birthday").val(ret.birthday);
        $("#tel_num").val(ret.tel_num);
        for (edu in ret.education) {
            var edu = ret.education[edu];
            $("#school").val(edu.school);
            $("#major").val(edu.major);
            $("#").val(edu.level);
            $("#graduation_date").val(edu.graduation_date)
        }

        for (exp in ret.experience) {
            var exp = ret.experience[exp];
            $("#company").val(exp.company);
            $("#job").val(exp.job);
            $("#job_date_start").val(exp.job_date_start);
            $("#job_date_end").val(exp.job_date_end);
            $("#job_content").val(exp.job_content);
        }

        $("#expect_job").val(ret.expect_job);
        $("#expect_salary").val(ret.expect_salary);
        $("#postscript").val(ret.postscript);

        $("#description").val(ret.description);

        if (ret.filename) {
            $("#download").text(ret.filename);
            $("#fileupload").addClass('hidden');
            $(".download").removeClass('hidden');
        }

        $("#del_file").click(function () {
            $("#file").attr("key", '');
            $("#file").attr("filename", '');
            $(".filename").text('请上传xls，xlsx，pdf， ppt， txt格式文件');
            $(".filename").removeClass('black');
            $("#file").attr("flag", 'false');
            $(".download").addClass('hidden');
            $("#download").text('');
            $("#fileupload").removeClass('hidden');
        });

    }
}

init_value();

initdate();


$("#file").change(function (event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function (event) {
        var data = event.target.result.slice(5, -2).split(",")[1];
        var filename = file.name;

        show_load();
        $.post("/api/upload/", {data: data}, function (msg) {
            if (!msg.error_code) {
                var file_key = msg.file_key;
                $("#file").attr("key", file_key);
                $("#file").attr("filename", filename);
                $(".filename").text(filename);
                $(".filename").addClass('black');
                $("#file").attr("flag", 'true');
                hide_load()
            } else {
                alert(msg.msg);
                $("#file").attr("flag", 'false');
            }
        });
    };

    reader.readAsDataURL(file);

});


$("#save").click(function () {

    var name = $("#name").val();
    var top = $("#info").offset().top;
    var left = $("#info").offset().left;
    if (!name) {

        window.scrollTo(top, left);
        $("#name").popover({trigger: "manual", content: "请输入姓名", placement: "top"});
        $("#name").popover("show");
        setTimeout(function () {
            $('#name').popover('destroy')
        }, 1500);
        return false
    }

    var birthday = $("#birthday").val();
    if (!birthday) {
        window.scrollTo(top, left);
        $("#birthday").popover({trigger: "manual", content: "请选择出生日期", placement: "top"});
        $("#birthday").popover("show");
        setTimeout(function () {
            $('#birthday').popover('destroy')
        }, 1500);
        return false
    }

    var tel = $("#tel_num").val();
    if (!tel) {
        window.scrollTo(top, left);
        $("#tel_num").popover({trigger: "manual", content: "请输入手机号", placement: "top"});
        $("#tel_num").popover("show");
        setTimeout(function () {
            $('#tel_num').popover('destroy')
        }, 1500);
        return false
    } else {
        if (!/1[3|4|5|7|8]\d{9}/.test(tel)) {
            window.scrollTo(top, left);
            $("#tel_num").popover({trigger: "manual", content: "手机号输入错误，请重新输入", placement: "top"});
            $("#tel_num").popover("show");
            setTimeout(function () {
                $('#tel_num').popover('destroy')
            }, 1500);
            return false
        }
    }

    var email = $("#email").val();
    if (!email) {
        window.scrollTo(top, left);
        $("#email").popover({trigger: "manual", content: "请输入邮箱地址", placement: "top"});
        $("#email").popover("show");
        setTimeout(function () {
            $('#email').popover('destroy')
        }, 1500);
        return false
    } else {
        if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/.test(email)) {
            window.scrollTo(top, left);
            $("#email").popover({trigger: "manual", content: "邮箱地址输入错误，请重新输入", placement: "top"});
            $("#email").popover("show");
            setTimeout(function () {
                $('#email').popover('destroy')
            }, 1500);
            return false
        }

    }

    var sex = $('input[type="radio"][name="sex"]:checked').val();

    var data = {
        name: name,
        birthday: birthday,
        tel: tel,
        sex: sex,
        email: email,

        school: $("#school").val(),
        major: $("#major").val(),
        level: $("#level").val(),
        graduation_date: $("#graduation_date").val(),

        company: $("#company").val(),
        job: $("#job").val(),
        job_date_start: $("#job_date_start").val(),
        job_date_end: $("#job_date_end").val(),
        job_content: $("#job_content").val(),

        expect_job: $("#expect_job").val(),
        expect_salary: $("#expect_salary").val(),
        postscript: $("#postscript").val(),


        description: $("#description").val(),
        file_key: $("#file").attr("key"),
        filename: $("#file").attr('filename')
    };

    $.post("/api/resume/", data, function (ret) {
        if (!ret.error_code) {
            window.location.href = '/resume_view/';
        } else {
            alert(ret.msg)
        }
        ;
    })
});


function hide_load() {
    if ($("#bonfire-pageloader").hasClass('hidden')) {
        return
    }
    ;
    $('#bonfire-pageloader').addClass('hidden');
}

function show_load() {
    var browserwidth = $(window).width();
    var browserheight = $(window).height();
    $('.bonfire-pageloader-icon').css('right', ((browserwidth - $(".bonfire-pageloader-icon").width()) / 2)).css('top', ((browserheight - $(".bonfire-pageloader-icon").height()) / 2));
    $('#bonfire-pageloader').removeClass('hidden');
};
