#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import commands
result = commands.execute('команды')
print(result)
print()

result = commands.execute('ругнись петр иваныч')
print(result)
print()

# result = commands.execute('спой')
# print(result)
# print()

# import requests
# rs = requests.get('http://127.0.0.1:55000/get_commands')
# rs = rs.json()
# print(rs)
# # for command, description in rs.items():
# #     print('{}: {}'.format(command, description))
# # print()
#
# print()
# rs = requests.get('http://127.0.0.1:55000/get_commands?as_result')
# rs = rs.json()
# print(rs)
#
# print()
# rs = requests.post('http://127.0.0.1:55000/execute', json={'command': 'ругнись петр иваныч'})
# print(rs.json())
