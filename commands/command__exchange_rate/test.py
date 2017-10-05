#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands import generate_request
from commands.command__exchange_rate.server import ExchangeRateServer
from db import get_execute_command_url_server

url = get_execute_command_url_server(ExchangeRateServer.guid)
command_name = 'курс валют'


import requests
rs = requests.post(url, json=generate_request(command_name))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name=command_name, command='ok'))
print(rs.json())
