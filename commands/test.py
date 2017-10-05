#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import commands
result = commands.execute('команды')
print(repr(result))
print()

result = commands.execute('курс валют')
print(repr(result))
print()

result = commands.execute('Курс ВАлут')
print(repr(result))
print()

result = commands.execute('насмеши')
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
