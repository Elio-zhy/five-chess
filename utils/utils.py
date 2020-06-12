#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@File       :   utils.py
@Time       :   20/06/04 12:48
@Author     :   Elio Zhou
"""

import uuid
import functools
import copy
import json
import numpy as np

from typing import Union, List
from geventwebsocket.websocket import WebSocket

from settings import MAX_ROOM, MAX_ONLINE_USER

EMPTY = 0
BLACK = 1
WHITE = 2


class User:
    def __init__(self, ws: WebSocket, name: str):
        self.ws = ws
        self.name = name
        self.uuid = uuid.uuid4().bytes.hex()
        # this field has following options: `online`, `room`, `gaming`
        self.status = 'online'
        self.room = None


class Room:
    def __init__(self):
        self.uuid = uuid.uuid4().bytes.hex()
        self.users: List[User] = []
        self.status = 'idle'
        self.board = np.zeros((10, 10), dtype=int)
        self.cur_player = None
        self.first_player = None
        self.count = 0
        self.game_init()

    def serialize(self):
        res = {
            'uuid': self.uuid,
            'users': list(map(lambda user: {'name': user.name, 'status': user.status}, self.users)),
            'status': self.status,
            'board': self.board.tolist(),
            'first_player': self.first_player
        }

        return res

    def broadcast(self):
        for user in self.users:
            user.ws.send(json.dumps({'room': self.serialize()}))

    def broadcast_board(self):
        for user in self.users:
            user.ws.send(json.dumps({'board': self.board.tolist()}))

    def game_init(self):
        self.board = np.zeros((10, 10), dtype=int)
        self.count = 0
        self.cur_player = None
        self.first_player = None
        self.status = 'idle'
        for user in self.users:
            user.status = 'in room'

    def cur_chess_color(self):
        if self.cur_player == self.first_player:
            return BLACK
        else:
            return WHITE

    def horizon_win(self, x: int, y: int):
        count = 1
        cur = self.board[y][x]
        # left side
        for i in range(x - 1, -1, -1):
            if self.board[y][i] == cur:
                count += 1
            else:
                break

        # right side
        for i in range(x + 1, 10, 1):
            if self.board[y][i] == cur:
                count += 1
            else:
                break

        return count >= 5

    def vertical_win(self, x: int, y: int):
        count: int = 1
        cur = self.board[y][x]
        # left side
        for i in range(y - 1, -1, -1):
            if self.board[i][x] == cur:
                count += 1
            else:
                break

        # right side
        for i in range(y + 1, 10, 1):
            if self.board[i][x] == cur:
                count += 1
            else:
                break

        return count >= 5

    def oblique_win(self, x: int, y: int):
        count_1: int = 1
        count_2: int = 1
        cur = self.board[y][x]
        # down-left side
        for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
            if self.board[j][i] == cur:
                count_1 += 1
            else:
                break

        # up-right side
        for i, j in zip(range(x + 1, 10, 1), range(y + 1, 10, 1)):
            if self.board[j][i] == cur:
                count_1 += 1
            else:
                break

        # down-right side
        for i, j in zip(range(x + 1, 10, -1), range(y - 1, -1, -1)):
            if self.board[j][i] == cur:
                count_2 += 1
            else:
                break

        # up-left side
        for i, j in zip(range(x - 1, -1, -1), range(y + 1, 10, 1)):
            if self.board[j][i] == cur:
                count_2 += 1
            else:
                break

        return count_1 >= 5 or count_2 >= 5

    def win(self, x: int, y: int):
        return self.horizon_win(x, y) or self.vertical_win(x, y) or self.oblique_win(x, y)


class Hall:
    def __init__(self):
        self.rooms = {}
        self.users = {}
        self.hall_init()

    def hall_init(self):
        for _ in range(10):
            room = Room()
            self.rooms[room.uuid] = room

        self.users = {}

    def rooms_serialize(self):
        res = list(
            map(lambda uid: {'uuid': uid, 'p_num': len(self.rooms[uid].users), 'status': self.rooms[uid].status},
                self.rooms))
        return res

    def broadcast_rooms(self):
        for ws in self.users:
            ws.send(json.dumps({'room-list': self.rooms_serialize(), 'online_num': len(self.users)}))
