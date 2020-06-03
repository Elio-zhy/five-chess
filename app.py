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
from flask_sockets import Sockets

from settings import BASE_DIR
from api import init_socket, init_api


def create_app():

    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

    # load configuration.
    app.config.from_pyfile(os.path.join(BASE_DIR, 'settings.py'))

    return app


if __name__ == '__main__':

    app = create_app()

    socket = Sockets(app)

    @socket.route('/echo')
    def echo_socket(ws):
        while not ws.closed:
            now = datetime.datetime.now().isoformat() + 'Z'
            ws.send(now)
            time.sleep(1)

    # init_socket(app)
    init_api(app)

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
