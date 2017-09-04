#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.get('http://127.0.0.1:55000/get_commands')
print(rs.json())

rs = requests.post('http://127.0.0.1:55000/execute', json={'command': 'Петя'})
print(rs.json())
