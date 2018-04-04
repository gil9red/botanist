#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import generate_request
from commands.command__weather_in_city.server import WeatherServer
from db import get_execute_command_url_server

url = get_execute_command_url_server(WeatherServer.guid)
command_name = 'погода'


import requests
rs = requests.post(url, json=generate_request(command_name, command='Магнитогорск'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='Челябинск'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='Москва'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command='3421выаы:)'))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, command=''))
print(rs.json())

rs = requests.post(url)
print(rs.json())
