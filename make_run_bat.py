#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


FILE_NAME_RUN = 'run.bat'
file_name_list = [
    'main_vk_bot.py',
    'commands\coordinator.py'
]

import glob
file_name_list += glob.glob('commands\command__*\server.py')

text_run = """
@echo off
REM Указание пути, чтобы модули при импортировании могли найти нужные им модули/пакеты
set PYTHON={python}

"""

import sys
text_run = text_run.format(python=sys.executable)

for file_name in file_name_list:
    text_run += 'start %PYTHON% ' + file_name + '\n'

text_run = text_run.strip()
print(text_run)

with open(FILE_NAME_RUN, mode='w', encoding='utf-8') as f:
    f.write(text_run)
