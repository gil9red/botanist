#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: пока выполняется запрос показывать текст с "Пожалуйста, подождите...", или просто какую нибудь крутящуюся фигню
# TODO: сделать кликабельный текст в описании команд и искать по шаблону регулярки текст вида:
#       Бот, калькулятор 2 + 2 * 2
#       Нужно чтобы команды и их текст стали кликабельными и при клике на них заполнялся и скроллился "Input command:"
#       "Бот, калькулятор 2 + 2 * 2" -> "калькулятор 2 + 2 * 2"
#
#       Кроме того, сами команды типо "тест гифку" тоже нужно сделать такими же кликабельными
# TODO: мб завести в команды отдельное поле "Примеры"? И там приводить примеры. Это удобнее чем парсить из описания


import pathlib
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
            result['stack_trace'] = traceback.format_exc()

            return result

        return rs

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_availability_coordinator(self):
        url = db.get_url_coordinator()
        if url:
            import requests

            try:
                requests.get(url, timeout=0.1)
                return {'ok': True, 'url': url}

            except requests.exceptions.ConnectionError:
                pass

        return {'ok': False, 'url': url}

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
