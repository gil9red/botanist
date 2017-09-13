#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# command = 'регнись петр иваныч регнись'
# command_name = 'регнись'
# word_list = command.split()
#
# for i in range(1, len(word_list) + 1):
#     print(i, word_list[:i], ' '.join(word_list[:i]))
#
#     if command_name == ' '.join(word_list[:i]):
#         print(command_name + ' ' + ' '.join(word_list[i:]))
#         break
#
# quit()

import commands
result = commands.execute('команды')
print(repr(result))
print()

result = commands.execute('ругнись петр иваныч')
print(repr(result))
print()

result = commands.execute('регнись петр иваныч')
print(repr(result))
print()

result = commands.execute('регнись регнись петр иваныч')
print(repr(result))
print()

result = commands.execute('регнись петр иваныч регнись')
print(repr(result))
print()

result = commands.execute('погода магнитогорск')
print(repr(result))
print()

result = commands.execute('пагода магнитогорск')
print(repr(result))
print()

result = commands.execute('курс валют')
print(repr(result))
print()


result = commands.execute('сила луны')
print(repr(result))
print()

result = commands.execute('2 + 2 = ?')
print(repr(result))
print()

result = commands.execute('спой')
print(repr(result))
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
