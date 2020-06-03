#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   __init__.py
@Time       :   20/06/03 20:36
@Author     :   Elio Zhou
"""

from flask_restful import Api
from flask_socketio import SocketIO

from api.v1.chess import init_api as chess_init_api
from api.v1.chess import init_socket as chess_init_socket


def create_api():
    api = Api(prefix='/api/v1')
    chess_init_api(api)

    return api


def create_socket():
    socket = SocketIO()
    chess_init_socket(socket)

    return socket
