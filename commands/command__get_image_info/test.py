#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
import pathlib
from common import generate_request, create_attachment, FileAttachment, AttachmentType
from commands.command__get_image_info.server import GetImageInfoServer
from db import get_execute_command_url_server

url = get_execute_command_url_server(GetImageInfoServer.guid)
command_name = 'получить информацию о картинке'


FILE_NAME = 'example.jpg'

with open(FILE_NAME, 'rb') as f:
    content = f.read()
    extension = pathlib.Path(FILE_NAME).suffix[1:]

attachment = FileAttachment(content=content, extension=extension)
attachment_type = AttachmentType.IMAGE

rs = requests.post(url, json=generate_request())
print(rs.json())

rs = requests.post(url, json=generate_request(command_name))
print(rs.json())

rs = requests.post(url, json=generate_request(command_name, attachment=create_attachment(attachment, attachment_type)))
print(rs.json())
print(rs.json()['result'])
