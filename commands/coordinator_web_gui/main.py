#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: брать таблицу серверов из ajax и показывать из базы информацию о них.
#       круто будет выглядеть когда на странице можно увидеть какие из серверов запущены,
#       а какие нет.

import sys


# TODO: возможность "свернуть" список команд, добавить кнопку "сворачивания"/"разворачивания" всех команд


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())
dir_up_up = str(current_dir.parent.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)

if dir_up_up not in sys.path:
    sys.path.append(dir_up_up)


STATIC_DIR = str((pathlib.Path(__file__).parent / "static").resolve())
INDEX_FILE_NAME = str((pathlib.Path(__file__).parent / "static" / 'index.html').resolve())


from commands import execute
import db

import cherrypy


class Root:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def execute(self):
        rq = cherrypy.request.json
        print(rq)

        command = rq['command']

        try:
            rs = execute(command)

        except Exception as e:
            import traceback

            from collections import OrderedDict
            result = OrderedDict()
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()

            return result

        return rs

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_all_server_with_commands(self):
        return {
            'server_headers': [
                'Название', 'GUID', 'Url', 'Доступность', 'Время последней доступности',
                'Дата последнего запроса к серверу', 'Полный путь к файлу сервера'
            ],
            'command_headers': ['Команда', 'Описание', 'Url'],
            'servers': db.get_all_server_with_commands(),
        }

    @cherrypy.expose
    def index(self):
        return open(INDEX_FILE_NAME, encoding='utf-8')


if __name__ == '__main__':
    # Set port
    cherrypy.config.update({'server.socket_port': 9090})

    # Autoreload off
    cherrypy.config.update({'engine.autoreload.on': False})

    # For include css, js in html
    cherrypy.config.update({
        'tools.staticdir.on': True,
        'tools.staticdir.dir': STATIC_DIR,
    })

    cherrypy.quickstart(Root())
