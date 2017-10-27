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
assert rs.json()['result'] == 'CFF0E8E2E5F220ECE8F021'

rs = requests.post(
    url + '/execute?hex2str',
    json=generate_request(command_name='hex2str', command='CFF0E8E2E5F220ECE8F021')
)
print(rs.json())
assert rs.json()['result'] == 'Привет мир!'

rs = requests.post(
    url + '/execute?str2bin',
    json=generate_request(command_name='str2bin', command='Привет мир!')
)
print(rs.json())
assert rs.json()['result'] == '11001111 11110000 11101000 11100010 11100101 11110010 ' \
                              '00100000 11101100 11101000 11110000 00100001'

rs = requests.post(
    url + '/execute?bin2str',
    json=generate_request(command_name='bin2str', command='11001111 11110000 11101000 11100010 11100101 11110010 '
                                                          '00100000 11101100 11101000 11110000 00100001')
)
print(rs.json())
assert rs.json()['result'] == 'Привет мир!'

# Специально вызываем ошибку
rs = requests.post(
    url + '/execute?hex2str',
    json=generate_request(command_name='hex2str', command='Привет мир!')
)
print(rs.json())
assert rs.json()['result'] is None
