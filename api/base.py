# coding=utf-8
from flask import Flask, json, request, current_app
from werkzeug.wrappers import Response

from api.utils import ApiResult
from api.exceptions import ApiException
from views import BaseView


class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, dict):
            if 'r' not in rv:
                rv['r'] = 1
            rv = ApiResult(rv)
        if isinstance(rv, ApiResult):
            return rv.to_response()
        return Flask.make_response(self, rv)


json_api = ApiFlask(__name__)
PER_PAGE = 20


@json_api.errorhandler(ApiException)
def api_error_handler(error):
    return error.to_result()


@json_api.errorhandler(403)
@json_api.errorhandler(404)
@json_api.errorhandler(500)
def error_handler(error):
    if hasattr(error, 'name'):
        msg = error.name
        code = error.code
    else:
        msg = error.message
        code = 500
    return ApiResult({'message': msg}, status=code)


class ApiView(BaseView):
    url_rule = ''
    view_name = 'home'

    def get(self):
        return



