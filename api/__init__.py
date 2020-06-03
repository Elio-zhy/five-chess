#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   __init__.py
@Time       :   20/06/03 20:35
@Author     :   Elio Zhou
"""

from api.v1 import create_api, create_socket


def init_api(app):
    api = create_api()

    api.init_app(app)


def init_socket(app):
    socket = create_socket()

    socket.init_app(app)
