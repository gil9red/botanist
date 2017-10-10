#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: использовать jsonschema для проверки запросов API
import typing
import common

# TODO: для отладки возвращать эхо из (command_name + " " + command).upper()
# TODO: удалить DEBUG_ALONE_COORDINATOR и использовать вместо него DEBUG

# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо
DEBUG = False
# DEBUG = True

# Если True, тогда координатор не отправляет команду, а сразу отвечает эхом
DEBUG_ALONE_COORDINATOR = False
# DEBUG_ALONE_COORDINATOR = True

# TODO: для logging.basicConfig определить filename для сбора всякие логов (проверить
#       как сработает для уже установленых логов)
# cherrypy.config.update({
#     # Для каждого сервера можно реализовать:
#     # Дополнительно можно к имени лога добавлять имя сервера и путь указывать полный, в корень проекта в папке logs
#     # Например: mini_vk_bot/logs
#     'log.access_file': "access.log",
#     'log.error_file': "error.log",
# })


# TODO: упросить результат функции
def execute(command: str, raw=False) -> typing.Union[dict, typing.Tuple[str, str], typing.Tuple[None, str]]:
    import db
    url = db.get_url_coordinator()

    import requests

    try:
        rs = requests.post(url, json=generate_request(command_name=None, command=command))
        print(rs.text)

    except requests.exceptions.ConnectionError:
        return 'Сервер Координатора ({}) недоступен'.format(url), common.TYPE_TEXT

    # На всякий случай, вдруг не json придет, а html
    try:
        rs = rs.json()
        print('rs:', rs)

        if raw:
            return rs

    except Exception as e:
        import traceback
        message = 'При выполнении команды "{}" произошла ошибка: ' \
                  '"{}":\n\n{}'.format(command, e, traceback.format_exc())

        print(message + '\n\nrs.content:\n{}'.format(rs.content))

        return message, common.TYPE_TEXT

    if rs['error'] is not None:
        return rs['error'], rs['type']

    return rs['result'], rs['type']


def generate_request(command_name: typing.Union[str, None], command: str=None) -> dict:
    return {
        'command_name': command_name,
        'command': command,
    }
