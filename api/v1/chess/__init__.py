#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   __init__.py
@Time       :   20/06/03 20:36
@Author     :   Elio Zhou
"""

from api.v1.chess.sockets import play_chess
from api.v1.chess.views import Index


def init_api(api):
    api.add_resource(Index, '/index')


def init_socket(socket):
    socket.add_url_rule('/play', None, play_chess)
