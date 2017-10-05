#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: для всех серверов ввести случайный порт

# TODO: команду hex2str и str2hex
# TODO: команды hex2str и str2hex реализовать на одном сервере: HexConverter
#       Мб через параметры задавать, типо /execute?hex2str и /execute?str2hex
#       нужно только пробрасывать параметры в нужные сервера

# TODO: использовать jsonschema для проверки запросов API

# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо
DEBUG = False
# DEBUG = True

# Если True, тогда координатор не отправляет команду, а сразу отвечает эхом
DEBUG_ALONE_COORDINATOR = False
# DEBUG_ALONE_COORDINATOR = True

# TODO: для logging.basicConfig определить filename для сбора всякие логов (проверить
#       как сработает для уже установленых логов)
# TODO: добавить флаг для app.debug = True


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
# TODO: команду bin2str и str2bin
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


def get_url_coordinator():
    from db import create_connect
    with create_connect() as connect:
        url = connect.execute(
            'SELECT Server.url || Command.uri FROM Command, Server '
            'WHERE Command.server_guid = :guid AND Server.guid = :guid ',

            #
            {'guid': 'B57B73C8F8D442C48EDAFC951963D7A5'}
        ).fetchone()[0]

        return url


def execute(command):
    url = get_url_coordinator()

    import requests
    rs = requests.post(url, json=generate_request(command))
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


def generate_request(command=None):
    return {
        'command': command,
    }
