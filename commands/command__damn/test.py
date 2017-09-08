#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request

import requests
rs = requests.post('http://127.0.0.1:55001/execute', json=generate_request('Петя'))
print(rs.json())

rs = requests.post('http://127.0.0.1:55001/execute', json={'status': 'ok'})
print(rs.json())

rs = requests.post('http://127.0.0.1:55001/execute', data=str({'status': 'ok'}))
print(rs.json())
