#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: использовать jsonschema для проверки запросов API
import typing


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


def execute(command: str) -> dict:
    import db
    url = db.get_url_command_coordinator()
    if not url:
        raise Exception('Не удалось получить адрес Координатора')

    import requests

    try:
        rs = requests.post(url, json=generate_request(command_name=None, command=command))
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


def generate_request(command_name: typing.Union[str, None], command: str=None) -> dict:
    return {
        'command_name': command_name,
        'command': command,
    }
