#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.post('http://127.0.0.1:55002/execute')
print(rs.json())

rs = requests.post('http://127.0.0.1:55002/execute', json={'command': 'ok'})
print(rs.json())
