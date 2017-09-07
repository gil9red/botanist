#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.post('http://127.0.0.1:55003/execute', json={'command': 'Магнитогорск'})
print(rs.json())

rs = requests.post('http://127.0.0.1:55003/execute', json={'command': '3421выаы:)'})
print(rs.json())

rs = requests.post('http://127.0.0.1:55003/execute', json={'command': ''})
print(rs.json())

