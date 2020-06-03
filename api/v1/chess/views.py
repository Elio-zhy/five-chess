#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   views.py
@Time       :   20/06/03 20:36
@Author     :   Elio Zhou
"""

from flask import request
from flask_restful import Resource


class Index(Resource):
    @staticmethod
    def get():
        return {'message': 'index'}
