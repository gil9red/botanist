#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: url для запросов тестов брать из базы
# TODO: использовать jsonschema для проверки запросов API

# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо
DEBUG = False
# DEBUG = True

# Если True, тогда координатор не отправляет команду, а сразу отвечает эхом
DEBUG_ALONE_COORDINATOR = False
# DEBUG_ALONE_COORDINATOR = True

# TODO: для logging.basicConfig определить filename для сбора всякие логов (проверить
#       как сработает для уже установленых логов)


# TODO: мб при ответе бота на команду выделять заголовок ответа подчеркиванием? т.е. бот после команды
#       пишет: "Результат выполнения команды <название команды>:\n<результат>" и это будет подчеркнуто
#   ИЛИ:
#       Пример: Бот: результат выполнения команды: "погода магнитогорск"
#               23 C, облачно
# TODO: завести в базе статистику команд таблицу в которой будет инфа о времени выполнения
#       и названии команды

def execute(command):
    import db
    url = db.get_url_coordinator()

    import requests
    rs = requests.post(url, json=generate_request(command_name=None, command=command))
    print(rs.text)

    try:
        rs = rs.json()
        print('rs:', rs)

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
