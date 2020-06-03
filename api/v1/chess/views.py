#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   views.py
@Time       :   20/06/03 20:36
@Author     :   Elio Zhou
"""

from flask import request, render_template, Response
from flask_restful import Resource


class Index(Resource):
    @staticmethod
    def get():
        return Response(render_template('index.html'), content_type='text/html')
