#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request

url = 'http://127.0.0.1:29314/execute'

import requests
rs = requests.post(url, json=generate_request(command_name='погода', command='Магнитогорск')
)
print(rs.json())

rs = requests.post(url, json=generate_request(command_name='погода', command='Челябинск')
)
print(rs.json())

rs = requests.post(url, json=generate_request(command_name='погода', command='Москва')
)
print(rs.json())

rs = requests.post(url, json=generate_request(command_name='погода', command='3421выаы:)')
)
print(rs.json())

rs = requests.post(url, json=generate_request(command_name='погода', command='')
)
print(rs.json())

rs = requests.post(url)
print(rs.json())
