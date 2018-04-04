#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import generate_request
from commands.command__damn.server import DamnServer
from db import get_execute_command_url_server

url = get_execute_command_url_server(DamnServer.guid)
command_name = 'ругнись'


import requests
rs = requests.post(url, json=generate_request(command_name=command_name, command='Петя'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name=command_name))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name=command_name, command=''))
print(rs.json())

rs = requests.post(url, json={'status': 'ok'})
print(rs.json())

rs = requests.post(url, data=str({'status': 'ok'}))
print(rs.json())
