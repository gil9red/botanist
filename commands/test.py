#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import common
result = common.execute('команды')
print(repr(result))
print()

result = common.execute('str2hex Привет мир!')
print(repr(result))
print()

result = common.execute('hex2str CFF0E8E2E5F220ECE8F021')
print(repr(result))
print()

result = common.execute('курс валют')
print(repr(result))
print()

result = common.execute('Курс ВАлут')
print(repr(result))
print()

result = common.execute('насмеши')
print(repr(result))
print()

result = common.execute('ругнись петр иваныч')
print(repr(result))
print()

result = common.execute('регнись петр иваныч')
print(repr(result))
print()

result = common.execute('регнись регнись петр иваныч')
print(repr(result))
print()

result = common.execute('регнись петр иваныч регнись')
print(repr(result))
print()

result = common.execute('погода магнитогорск')
print(repr(result))
print()

result = common.execute('пагода магнитогорск')
print(repr(result))
print()

result = common.execute('курс валют')
print(repr(result))
print()


result = common.execute('сила луны')
print(repr(result))
print()

result = common.execute('2 + 2 = ?')
print(repr(result))
print()

result = common.execute('спой')
print(repr(result))
print()
