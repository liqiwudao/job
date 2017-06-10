# -*- coding:utf-8 -*-

# import json
#
# import re
#
# from flask import request, make_response
#
# from views import BaseView
# from uploader import Uploader
#
#
# from flask import request, make_response
#
# from finance.views import BaseAdminView
#
# from daisy.views.decorators import templated, template_context

# class UploadView(BaseView):
#
#     def post(self):
#         mimetype = 'application/json'
#         result = {}
#         action = request.args.get('action')
#         # 解析JSON格式的配置文件
#         with open('config.json', 'rb') as fp:
#             try:
#                 # 删除 `/**/` 之间的注释
#                 CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
#             except:
#                 CONFIG = {}
#
#         # UPLOAD_FOLDER = 'static/'
#         UPLOAD_FOLDER = 'static/'
#
#         if action == 'config':
#             # 初始化时，返回配置文件给客户端
#             result = CONFIG
#         elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
#             if action == 'uploadimage':
#                 fieldName = CONFIG.get('imageFieldName')
#                 config = {
#                     "pathFormat": CONFIG['imagePathFormat'],
#                     "maxSize": CONFIG['imageMaxSize'],
#                     "allowFiles": CONFIG['imageAllowFiles']
#                 }
#             elif action == 'uploadvideo':
#                 fieldName = CONFIG.get('videoFieldName')
#                 config = {
#                     "pathFormat": CONFIG['videoPathFormat'],
#                     "maxSize": CONFIG['videoMaxSize'],
#                     "allowFiles": CONFIG['videoAllowFiles']
#                 }
#             else:
#                 fieldName = CONFIG.get('fileFieldName')
#                 config = {
#                     "pathFormat": CONFIG['filePathFormat'],
#                     "maxSize": CONFIG['fileMaxSize'],
#                     "allowFiles": CONFIG['fileAllowFiles']
#                 }
#             if fieldName in request.files:
#                 field = request.files[fieldName]
#                 uploader = Uploader(field, config, UPLOAD_FOLDER)
#                 result = uploader.getFileInfo()
#             else:
#                 result['state'] = '上传接口出错'
#
#         elif action in ('uploadscrawl'):
#             # 涂鸦上传
#             fieldName = CONFIG.get('scrawlFieldName')
#             config = {
#                 "pathFormat": CONFIG.get('scrawlPathFormat'),
#                 "maxSize": CONFIG.get('scrawlMaxSize'),
#                 "allowFiles": CONFIG.get('scrawlAllowFiles'),
#                 "oriName": "scrawl.png"
#             }
#             if fieldName in request.form:
#                 field = request.form[fieldName]
#                 uploader = Uploader(field, config, UPLOAD_FOLDER, 'base64')
#                 result = uploader.getFileInfo()
#             else:
#                 result['state'] = '上传接口出错'
#         elif action in ('catchimage'):
#             config = {
#                 "pathFormat": CONFIG['catcherPathFormat'],
#                 "maxSize": CONFIG['catcherMaxSize'],
#                 "allowFiles": CONFIG['catcherAllowFiles'],
#                 "oriName": "remote.png"
#             }
#             fieldName = CONFIG['catcherFieldName']
#             if fieldName in request.form:
#                 # 这里比较奇怪，远程抓图提交的表单名称不是这个
#                 source = []
#             elif '%s[]' % fieldName in request.form:
#                 # 而是这个
#                 source = request.form.getlist('%s[]' % fieldName)
#             _list = []
#             for imgurl in source:
#                 uploader = Uploader(imgurl, config, UPLOAD_FOLDER, 'remote')
#                 info = uploader.getFileInfo()
#                 _list.append({
#                     'state': info['state'],
#                     'url': info['url'],
#                     'original': info['original'],
#                     'source': imgurl,
#                 })
#             result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
#             result['list'] = _list
#         else:
#             result['state'] = '请求地址出错'
#
#
#         result = json.dumps(result)
#
#         if 'callback' in request.args:
#             callback = request.args.get('callback')
#             if re.match(r'^[\w_]+$', callback):
#                 result = '%s(%s)' % (callback, result)
#                 mimetype = 'application/javascript'
#             else:
#                 result = json.dumps({'state': 'callback参数不合法'})
#
#         res = make_response(result)
#         res.mimetype = mimetype
#         res.headers['Access-Control-Allow-Origin'] = '*'
#         res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
#         return res



