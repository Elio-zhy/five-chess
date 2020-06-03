#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   __init__.py
@Time       :   20/06/03 20:36
@Author     :   Elio Zhou
"""

from api.v1.chess.sockets import test_message, test_message_2, test_connect, test_disconnect
from api.v1.chess.views import Index


def init_api(api):
    api.add_resource(Index, '/index')


def init_socket(socket):
    socket.on_event('my event', test_message, '/test')

    socket.on_event('my broadcast event', test_message_2, '/test')

    socket.on_event('connect', test_connect, '/test')

    socket.on_event('disconnect', test_disconnect, '/test')
