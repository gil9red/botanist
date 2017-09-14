#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import commands
print(commands)
print(__file__)

import os
dir_name = os.path.dirname(__file__)
print(dir_name)
print()

file_name_server_wildcard = os.path.normpath(dir_name + '/command__*/*_server.py')

import glob
for file_name in glob.glob(file_name_server_wildcard):
    print(file_name)


