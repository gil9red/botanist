#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import generate_request
from commands.command__fun.server import FunServer
from db import get_execute_command_url_server

url = get_execute_command_url_server(FunServer.guid)
command_name = 'насмеши'


import requests
rs = requests.post(url, json=generate_request(command_name))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='ok'))
print(rs.json())
