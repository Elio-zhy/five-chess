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
import uuid
import json
import random

from flask import g
from geventwebsocket.websocket import WebSocket

from settings import MAX_ONLINE_USER
from settings import MAX_ROOM
from utils.utils import Hall, Room, User


init_board = [[0] * 10] * 10

hall = Hall()


def play_chess(ws: WebSocket):
    while not ws.closed:
        try:
            # receive message.
            message: str = ws.receive()

            if message is None:
                continue

            # message format: `action data`
            message: list = message.split(' ')

            # 连接大厅
            if message[0] == 'connect':
                # 已经在大厅里
                if ws in hall.users:
                    ws.send(json.dumps({'alert': 'already online'}))
                    continue

                # 进入大厅
                hall.users.update({ws: User(ws, message[1])})
                hall.broadcast_rooms()

            # 进入房间
            elif message[0] == 'enter':
                user = hall.users[ws]
                room = hall.rooms[message[1]]
                if user.room is not None:
                    hall.rooms[user.room].users.remove(user)
                user.status = 'in room'
                user.room = room.uuid

                # 房间满了
                if len(room.users) == 2:
                    ws.send(json.dumps({'alert': 'full'}))
                    continue

                # 房间里有一个人
                elif len(room.users) == 1:
                    room.users.append(user)
                    room.broadcast()
                    hall.broadcast_rooms()

                # 房间里没人
                else:
                    room.users.append(user)
                    room.broadcast()
                    hall.broadcast_rooms()

            # 准备
            elif message[0] == 'ready':
                user = hall.users[ws]
                room = hall.rooms[user.room]
                user.status = 'ready'

                # 房间还有其他人
                if len(room.users) == 2:
                    another_index = 1 - room.users.index(user)
                    room.users[another_index].ws.send(json.dumps({'info': room.users[another_index].name + ' ready'}))
                    room.broadcast()

                    # 对方也准备了，开始游戏
                    if room.users[another_index].status == 'ready':
                        room.status = 'gaming'
                        room.first_player = random.randint(0, 1)
                        room.cur_player = room.first_player
                        hall.broadcast_rooms()
                        room.users[room.first_player].ws.send(json.dumps({'alert': '你先手'}))
                        room.users[1 - room.first_player].ws.send(json.dumps({'alert': '你后手'}))

            # 下棋
            elif message[0] == 'put':
                user = hall.users[ws]
                room = hall.rooms[user.room]

                if user == room.users[room.cur_player]:
                    room.count += 1
                    color = room.cur_chess_color()
                    room.board[int(message[2])][int(message[1])] = color
                    room.cur_player = 1 - room.cur_player
                    for user in room.users:
                        user.ws.send(json.dumps({'board': room.board.tolist()}))
                    if room.win(int(message[1]), int(message[2])):
                        room.game_init()
                        winner = user.name
                        for user in room.users:
                            user.ws.send(json.dumps({'result': winner + ' win'}))
                            user.ws.send(json.dumps({'room': room.serialize()}))
                        room.users[0].status = 'in room'
                        room.users[1].status = 'in room'
                        hall.broadcast_rooms()
                        continue
                    elif room.count == 100:
                        room.game_init()
                        for user in room.users:
                            user.ws.send(json.dumps({'result': 'draw'}))
                            user.ws.send(json.dumps({'room': room.serialize()}))
                        room.users[0].status = 'in room'
                        room.users[1].status = 'in room'
                        room.status = 'idle'
                        hall.broadcast_rooms()
                        continue
            elif message[0] == 'leave':
                user = hall.users[ws]
                room = hall.rooms[user.room]

                room.users.remove(user)
                user.status = 'online'
                user.room = None
                room.game_init()
                hall.broadcast_rooms()
                room.broadcast()
        except Exception as e:
            print(str(e))

    user = hall.users[ws]

    if user.room is not None:
        room = hall.rooms[user.room]
        room.users.remove(user)
        room.game_init()

        for user in room.users:
            user.ws.send(json.dumps({'room': room.serialize()}))

    del hall.users[ws]
    hall.broadcast_rooms()
