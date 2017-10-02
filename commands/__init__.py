#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: использовать jsonschema для проверки запросов API
# TODO: пусть каждый вебсервер при запуске пишет в консоль свое название
# TODO: Добавить requirements.txt с списком используемых посторонних модулей, чтобы проще было устанавливать зависимости
#       Для установки зависимостей: pip install -r requirements.txt
#       http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/


# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо
DEBUG = False
# DEBUG = True

# Если True, тогда координатор не отправляет команду, а сразу отвечает эхом
DEBUG_ALONE_COORDINATOR = False
# DEBUG_ALONE_COORDINATOR = True

# TODO: для logging.basicConfig определить filename для сбора всякие логов (проверить
#       как сработает для уже установленых логов)
# TODO: добавить флаг для app.debug = True
# TODO: переименовать файлы серверов команд в server.py: damn_server.py -> server.py.
#       Подправить шаблон поиска в make_run_bat.py
# TODO: координатор, при недоступности сервера команды должен, отвечает что сервер такой-то команды
#       недоступен


# TODO: добавить команды текстовой обработки: нижнее подчеркивание, зачеркивание и т.п.
#       используя юникод. Пример: Вася -> В̶а̶с̶я
# TODO: мб при ответе бота на команду выделять заголовок ответа подчеркиванием? т.е. бот после команды
#       пишет: "Результат выполнения команды <название команды>:\n<результат>" и это будет подчеркнуто
#   ИЛИ:
#       Пример: Бот: результат выполнения команды: "погода магнитогорск"
#               23 C, облачно

# TODO: добавить в бота команду конвертации ghbdtn в привет
# TODO: Бот, подсчитай 2 + 2 * 2
# TODO: добавить команду ROT13
# TODO: добавить команду курс криптовалют
# TODO: добавить команду Язык Йода: http://vexer.ru/jokez/joda.php
# TODO: добавить команду для генерации в язык падонков
# TODO: добавить команду для генерации в старый православный язык
# TODO: добавить команду конвертирования, приложенной картинки в команде, в ascii графику
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
# TODO: 'что посмотреть': 'Рандомная ссылка на кинопоиск'
# TODO: 'котики': ':3',


# TODO: перенести настройки в базу
from collections import namedtuple
CommandModule = namedtuple('CommandModule', ['command', 'url', 'description'])

ALL_COMMAND_MODULE = [
    CommandModule(
        'команды',
        'http://127.0.0.1:55000/execute',
        'Показать список команд'
    ),
    CommandModule(
        'ругнись',
        'http://127.0.0.1:55001/execute',
        'Напиши кого бот отругает. Например: Бот, ругнись петр иваныч'
    ),
    CommandModule(
        'насмеши',
        'http://127.0.0.1:55002/execute',
        'Случайная цитата башорга'
    ),
    CommandModule(
        'погода',
        'http://127.0.0.1:55003/execute',
        'Погода в указанном населенном пункте. Например: Бот, погода магнитогорск'
    ),
]
ALL_COMMAND_BY_URL = {x.command: x.url for x in ALL_COMMAND_MODULE}
ALL_COMMAND_NAME_BY_DESCRIPTION = {x.command: x.description for x in ALL_COMMAND_MODULE}


def execute(command):
    import requests
    rs = requests.post('http://127.0.0.1:55000/execute', json=generate_request(command))
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


def generate_response(result=None, ok=True, error=None):
    return {
        'result': result,
        'ok': ok,
        'error': error,
    }


def generate_request(command):
    return {
        'command': command,
    }


def get_request_data(request_flask):
    request_text = request_flask.data.decode('utf-8')
    print('request_text:', request_text)

    import json
    rq = json.loads(request_text)
    print('rq:', rq)

    if 'command' not in rq:
        raise Exception("В запросе не найдено поле 'command'.")

    return rq
