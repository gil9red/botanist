#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request


import requests
rs = requests.post('http://127.0.0.1:55003/execute', json=generate_request('Магнитогорск'))
print(rs.json())

rs = requests.post('http://127.0.0.1:55003/execute', json=generate_request('3421выаы:)'))
print(rs.json())

rs = requests.post('http://127.0.0.1:55003/execute', json=generate_request(''))
print(rs.json())

rs = requests.post('http://127.0.0.1:55003/execute')
print(rs.json())
