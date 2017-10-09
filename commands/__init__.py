#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: использовать jsonschema для проверки запросов API

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


def execute(command, raw=False):
    import db
    url = db.get_url_coordinator()

    import requests
    try:
        rs = requests.post(url, json=generate_request(command_name=None, command=command))
        print(rs.text)

        rs = rs.json()
        print('rs:', rs)

        if raw:
            return rs

    except requests.exceptions.ConnectionError:
        return 'Сервер Координатора ({}) недоступен'.format(url)

    except Exception as e:
        import traceback
        print(e, traceback.format_exc(), rs.content)
        return

    if rs['error'] is not None:
        return rs['error']

    return rs['result']


def generate_request(command_name, command=None):
    return {
        'command_name': command_name,
        'command': command,
    }
