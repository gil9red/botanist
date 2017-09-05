#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо
DEBUG = False
# DEBUG = True


# TODO: каждая команда отдельный http вебсервер, к которым бот шлет запросы в формате json
# TODO: добавить команду курс валют
# TODO: добавить команду курс криптовалют
# TODO: поддержать опциональную команду график к командам курса валют, которая вернет картинку с графиком курса
#       диапазон курса выбрать опытным путем
# TODO: добавить команду поиска на торрентах, которая вернет ссылку на .torrent файл
# TODO: добавить команду для возврата гифки из https://giphy.com/ (https://developers.giphy.com/)
#       аналог такого делает бот битрикса. Команды поиска похоже нужно будет переводить на английский
# TODO: команда превращения ссылки в короткую (пусть будет выбор через какой сервис сокращать ссылку)
# TODO: команду hex2str и str2hex
# TODO: команду gin2str и str2bin
# TODO: команду генерации qrcode, который или ссылкой возвращается или как картинка
# TODO: команду возврата поздравления к др/юбилею для папы/мамы/бабушки и т.п.
# TODO: команды генерации в base64 и раскодирования из base64
# TODO: команду добавления напоминаний, типа "Бот, напомни о встрече у Ленина в 12:30"
# TODO: команду угадывания что на картинке
# TODO: команду ретуши фотографии -- например faceapp умеет добавлять улыбку и т.п.
# TODO: завести в базе статистику команд таблицу в которой будет инфа о времени выполнения
#       и названии команды

# TODO: remove
# ALL_COMMANDS = {
#     'насмеши': 'Случайная цитата башорга',
#     'ругнись': 'Напиши кого бот отругает. Например: "Бот, ругнись петр иваныч"',
#     'погода': 'Погода в указанном населенном пункте. Например: "Бот, погода магнитогорск" или '
#               '"бот, погода село кукуево"',
#     # 'что посмотреть': 'Рандомная ссылка на кинопоиск',
#     # 'котики': ':3',
#     'команды': 'Показать список команд',
# }

# TODO: перенести настройки в базу
from collections import namedtuple
CommandModule = namedtuple('CommandModule', ['command', 'url', 'description'])

ALL_COMMAND_MODULE = [
    CommandModule(
        'команды',
        'http://127.0.0.1:55000/get_commands?as_result',
        'Показать список команд'
    ),
    CommandModule(
        'ругнись',
        'http://127.0.0.1:55001/execute',
        'Напиши кого бот отругает. Например: "Бот, ругнись петр иваныч"'
    ),
    CommandModule(
        'насмеши',
        'http://127.0.0.1:55002/execute',
        'Случайная цитата башорга'
    ),
    CommandModule(
        'погода',
        'http://127.0.0.1:55003/execute',
        'Погода в указанном населенном пункте. Например: "Бот, погода магнитогорск" '
        'или "бот, погода село кукуево"'
    ),
]
ALL_COMMAND_BY_URL = {x.command: x.url for x in ALL_COMMAND_MODULE}
ALL_COMMAND_NAME_BY_DESCRIPTION = {x.command: x.description for x in ALL_COMMAND_MODULE}


def execute(command):
    import requests
    rs = requests.post('http://127.0.0.1:55000/execute', json={'command': command})
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


# def execute(command):
#     # TODO: кроме результата команды лучше писать что за команда
#     # Пример: Бот: результат выполнения команды: "погода магнитогорск"
#     #         23 C, облачно
#     #
#     # Любой ответ от бота нужно начинать с "Бот: "
#
#     # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки
#     if not any(command.lower().startswith(x) for x in ALL_COMMANDS):
#         return 'Получена неизвестная команда "{}".\n' \
#                'Чтобы узнать команды введи: "Бот, команды"'.format(command)
#
#     else:
#         message = ''
#
#         # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
#         execute_command = command.lower()
#
#         if execute_command.startswith('команды'):
#             return '\n'.join('{}: {}'.format(k, v) for k, v in ALL_COMMANDS.items())
#
#         elif execute_command.startswith('насмеши'):
#             from commands.command__fun import fun
#             return fun.get_random_quote()
#
#         elif execute_command.startswith('ругнись'):
#             # Вытаскивание имени того, кого нужно обругать
#             name = command[len('ругнись'):].strip()
#             if not name:
#                 name = 'Бот'
#
#             from commands.command__damn import damn
#             return damn.damn(name)
#
#         elif execute_command.startswith('погода'):
#             city = command[len('погода'):].strip()
#             if not city:
#                 return "Неправильная команда 'погода': не указан населенный пункт"
#
#             from commands.command__weather_in_city import weather_in_city
#             return weather_in_city.get_weather(city)
#
#     return message


# TODO: нужно стандартизировать формат запросов и ответов между модулями-командами

def generate_response(result=None, ok=True, error=None):
    return {
        'result': result,
        'ok': ok,
        'error': error,
    }

# class Request:
#     def __init__(self, command):
#         self.command = command
#
#     def to_json_str(self):
#         return {
#             'command': self.command,
#         }
#
#     @staticmethod
#     def from_json(json):
#         return Request(json['command'])
#
#
# class Response:
#     def __init__(self, response):
#         self.response = response
#
#     def to_json_str(self):
#         return {
#             'response': self.response,
#         }
#
#     @staticmethod
#     def from_json(json):
#         return Response(json['response'])
