#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  # 引用sys模块进来，并不是进行sys的第一次加载

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

import config
from base import create_app

app = create_app(__name__, config, template_folder='template', static_folder='static')
#
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8011, debug=True)
