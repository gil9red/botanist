#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: использовать jsonschema для проверки запросов API
import typing
import sys


# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо в верхнем регистре
DEBUG = False
# DEBUG = True

# TODO: для logging.basicConfig определить filename для сбора всякие логов (проверить
#       как сработает для уже установленых логов)
# cherrypy.config.update({
#     # Для каждого сервера можно реализовать:
#     # Дополнительно можно к имени лога добавлять имя сервера и путь указывать полный, в корень проекта в папке logs
#     # Например: mini_vk_bot/logs
#     'log.access_file': "access.log",
#     'log.error_file': "error.log",
# })


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)


from common import generate_request


def execute(command: str) -> dict:
    import db
    url = db.get_url_command_coordinator()
    if not url:
        raise Exception('Не удалось получить адрес Координатора')

    import requests

    try:
        rs = requests.post(url, json=generate_request(command=command))
        print(rs.text)

    except requests.exceptions.ConnectionError:
        raise Exception('Сервер Координатора ({}) недоступен'.format(url))

    # На всякий случай, вдруг не json придет, а html
    try:
        rs = rs.json()
        print('rs:', rs)

        return rs

    except Exception as e:
        import traceback
        message = 'При выполнении команды "{}" произошла ошибка: ' \
                  '"{}":\n\n{}'.format(command, e, traceback.format_exc())

        print(message + '\n\nrs.content:\n{}'.format(rs.content))

        raise Exception(message)
