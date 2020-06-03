#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   sockets.py
@Time       :   20/06/03 20:42
@Author     :   Elio Zhou
"""

import logging

from flask import g
from flask_socketio import emit


def test_message(message):
    emit('my response', {'data': message['data']})


def test_message_2(message):
    emit('my response', {'data': message['data']}, broadcast=True)


def test_connect():
    emit('my response', {'data': 'Connected'})


def test_disconnect():
    print('Client disconnected')
