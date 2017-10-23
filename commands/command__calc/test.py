#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request
from commands.command__calc.server import CalcServer
from db import get_execute_command_url_server

url = get_execute_command_url_server(CalcServer.guid)
command_name = 'калькулятор'


import requests
rs = requests.post(url, json=generate_request(command_name))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='2 + 2'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='2 + 2 * 2'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='10 ** 3'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='sin(2 ** 10)'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='(0xFF + 255) / 0b1010'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='(0xFF + 255) // 0b1010'))
print(rs.json())
