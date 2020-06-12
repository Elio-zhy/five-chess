#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   app.py
@Time       :   20/06/03 20:19
@Author     :   Elio Zhou
"""

import os
import datetime
import time

from flask import Flask

from settings import BASE_DIR
from api import init_socket, init_api


def create_app():
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'),
                static_folder=os.path.join(BASE_DIR, 'static'), static_url_path='')

    # load configuration.
    app.config.from_pyfile(os.path.join(BASE_DIR, 'settings.py'))

    return app


if __name__ == '__main__':
    app = create_app()

    init_socket(app)
    init_api(app)

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
