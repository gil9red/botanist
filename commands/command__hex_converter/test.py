#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request

url = 'http://127.0.0.1:9090'

import requests
rs = requests.post(
    url + '/execute?str2hex',
    json=generate_request(command_name='str2hex', command='Привет мир!')
)
print(rs.json())

import requests
rs = requests.post(
    url + '/execute?hex2str',
    json=generate_request(command_name='hex2str', command='CFF0E8E2E5F220ECE8F021')
)
print(rs.json())

import requests
rs = requests.post(
    url + '/execute?hex2str',
    json=generate_request(command_name='hex2str', command='Привет мир!')
)
print(rs.json())
