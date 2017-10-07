#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request
from commands.command__text_converter.server import TextConverter
from db import get_url_server

url = get_url_server(TextConverter.guid)


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
