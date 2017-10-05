#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request

url = 'http://127.0.0.1:55004/execute'

import requests
rs = requests.post(url, json=generate_request(command_name='курс валют'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name='курс валют', command='ok'))
print(rs.json())
