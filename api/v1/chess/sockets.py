#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   sockets.py
@Time       :   20/06/03 20:42
@Author     :   Elio Zhou
"""

import time
import logging
import datetime

from flask import g
from flask_sockets import Sockets


def echo_socket(ws):
    while not ws.closed:
        now = datetime.datetime.now().isoformat() + 'Z'
        ws.send(now)
        time.sleep(1)
