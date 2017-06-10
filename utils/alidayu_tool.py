# -*- coding: utf-8 -*-
from alidayu import api, appinfo

appkey = '23488569'

secret = 'bf8202a167e4f24b096eb37336a02080'

req = api.AlibabaAliqinFcSmsNumSendRequest()
req.set_app_info(appinfo(appkey, secret))


def send_code(phone, num):
    req.sms_type = "normal"
    req.sms_free_sign_name = "同创作"
    req.sms_param = {"number": num}
    req.rec_num = int(phone)
    req.sms_template_code = "SMS_24760140"
    resp = req.getResponse()
    return resp
