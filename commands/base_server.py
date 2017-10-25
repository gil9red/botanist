#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time
import typing
import sys


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)


from collections import namedtuple
Command = namedtuple('Command', ['name', 'uri', 'description', 'priority'])
Command.__new__.__defaults__ = (None, None, None, 0)

import db
import common
common.make_backslashreplace_console()

from commands import DEBUG

# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


# TODO: проверить все места с .json() -- нужно сделать так, чтобы у данных сохранялся порядок полей,
#       а т.к. .json() возвращает простой словарь, то поэтому порядок не сохраняется
#       Как вариант, можно ответ от requests парсить через стандартный модуль json,
#       добавляя небольшую доработку: https://stackoverflow.com/questions/6921699


class BaseServer:
    expose = cherrypy.expose
    json_in = cherrypy.tools.json_in()
    json_out = cherrypy.tools.json_out()
    request = cherrypy.request

    name = 'BaseServer'

    # Для генерации GUID нужно вызвать:
    # import uuid
    # x = uuid.uuid4()
    # print(x.hex.upper())
    #
    guid = 'E72DD28502D64F76B5E698DC9247C220'

    # Список команд, которые поддерживает сервер
    command_list = []

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def __init__(self):
        # Set a custom response for errors.
        self._cp_config = {'error_page.default': self.all_exception_handler}

        self.host = None
        self.port = None
        self.url = None

        cherrypy.engine.subscribe('start', self.on_start)

        self.last_elapsed = None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self) -> dict:
        return {
            'name': self.name,
            'guid': self.guid,
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def execute(self, **params) -> dict:
        db.update_datetime_last_request(self)

        try:
            rq = cherrypy.request.json
        except:
            raise Exception('Метод execute должен быть вызван через POST и содержать в запросе JSON!')

        print('[{}] Request: {}'.format(self.name, rq))

        if 'command' not in rq:
            raise Exception("В запросе не найдено поле 'command'.")

        if 'command_name' not in rq:
            raise Exception("В запросе не найдено поле 'command_name'.")

        command = rq['command']
        command_name = rq['command_name']

        print('_execute_body(command="{}", command_name="{}", **params={})'.format(command, command_name, params))

        start_elapsed = time.clock()

        try:
            # Для всех серверов, кроме Координатора возвращается дебажное сообщение.
            # Т.е. только Координатор обрабатывает запрос "как надо", а остальные, кто получит
            # сообщение вернут эхо
            # 'B57B73C8F8D442C48EDAFC951963D7A5' -- Координатор
            if DEBUG and self.guid != 'B57B73C8F8D442C48EDAFC951963D7A5':
                rs = '{} {}'.format(command_name, command).upper()
            else:
                rs = self._execute_body(command, command_name, **params)

        finally:
            self.last_elapsed = '{:.7f}'.format(time.clock() - start_elapsed)
            print('  Elapsed time: {} secs'.format(self.last_elapsed))

        # Если в ответе пришел не словарь
        if not isinstance(rs, dict):
            rs = self.generate_response(result=str(rs))

        rs['elapsed'] = self.last_elapsed

        if DEBUG:
            print('[{}] Response[DEBUG]: {}'.format(self.name, rs))
        else:
            print('[{}] Response: {}'.format(self.name, rs))

        return rs

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        raise Exception('_execute_body is not implemented!')

    def generate_response(self, result=None, attachment=None, error=None, traceback=None,
                          elapsed=None, data_type=common.DataType.TEXT) -> dict:
        if attachment:
            attachment = common.create_attachment(attachment, data_type)

        from collections import OrderedDict
        rs = OrderedDict()
        rs['result'] = result
        rs['attachment'] = attachment
        rs['error'] = error
        rs['type'] = data_type
        rs['traceback'] = traceback
        rs['server_name'] = self.name
        rs['server_guid'] = self.guid
        rs['elapsed'] = elapsed

        return rs

    def on_start(self):
        def _wait_server_running():
            import time

            # Wait running
            while not cherrypy.server.running:
                time.sleep(0.1)

            self.host, self.port = cherrypy.server.bound_addr
            self.url = cherrypy.server.description

            print('Started server "{}": {}:{} / {}'.format(self.name, self.host, self.port, self.url))
            print('Commands ({}):'.format(len(self.command_list)))
            for command in self.command_list:
                print('    {}'.format(command))

            # Иначе может не вывести сразу в консоль
            sys.stdout.flush()

            db.fill_server_info(self)

        from threading import Thread
        thread = Thread(target=_wait_server_running)
        thread.start()

    def all_exception_handler(self, status, message, traceback, version) -> dict:
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'

        error_text = traceback.strip().split('\n')[-1]
        error_text = error_text.split(':', maxsplit=1)[1].strip()
        print('[{}] Error: {}\n\n{}'.format(self.name, error_text, traceback))

        rs = self.generate_response(
            error=error_text,
            traceback=traceback,
            elapsed=self.last_elapsed,
        )

        import json
        return json.dumps(rs)

    def _before_run(self):
        pass

    def run(self, port=0):
        print('Start {}, port={}'.format(self.name, port))

        # Set port
        cherrypy.config.update({'server.socket_port': port})

        # Autoreload off
        cherrypy.config.update({'engine.autoreload.on': False})

        self._before_run()

        try:
            cherrypy.quickstart(self)

        finally:
            print('Finish server "{}": port={}'.format(self.name, port))


if __name__ == '__main__':
    server = BaseServer()
    server.run()
