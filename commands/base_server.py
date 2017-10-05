#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# pip install cherrypy
# https://github.com/cherrypy/cherrypy

import cherrypy


from collections import namedtuple
Command = namedtuple('Command', ['command', 'uri', 'description'])


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

    def __init__(self):
        # Set a custom response for errors.
        self._cp_config = {'error_page.default': self.all_exception_handler}

        self.host = None
        self.port = None
        self.url = None

        cherrypy.engine.subscribe('start', self.on_start)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {
            'name': self.name,
            'guid': self.guid,
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def execute(self):
        try:
            rq = cherrypy.request.json
        except:
            raise Exception('Метод execute должен быть вызван через POST и содержать в запросе JSON!')

        print('[{}] Request: {}'.format(self.name, rq))

        if 'command' not in rq:
            raise Exception("В запросе не найдено поле 'command'.")

        command = rq['command']

        rs = self._execute_body(command)
        print('[{}] Response: {}'.format(self.name, rs))

        if type(rs) == str:
            rs = self.generate_response(
                result=rs,
                ok=True,
            )

        return rs

    def _execute_body(self, command):
        raise Exception('_execute_body is not implemented!')

    def generate_response(self, result=None, ok=True, error=None, traceback=None):
        from collections import OrderedDict
        rs = OrderedDict()
        rs['result'] = result
        rs['ok'] = ok
        rs['error'] = error
        rs['traceback'] = traceback
        rs['server_name'] = self.name
        rs['server_guid'] = self.guid

        return rs

    def on_start(self):
        def _wait_server_running():
            import time

            # Wait running
            while not cherrypy.server.running:
                time.sleep(0.1)

            self.host, self.port = cherrypy.server.bound_addr
            self.url = cherrypy.server.description

            print('Start server "{}": {}:{} / {}'.format(self.name, self.host, self.port, self.url))
            print('    {}'.format(self.command_list))

            # TODO: обернуть в db.py как функцию
            import db
            with db.create_connect() as connect:
                # Если не существует, добавляем запись
                exist = connect.execute("SELECT 1 FROM Server WHERE guid = ?", (self.guid,)).fetchone()
                if not exist:
                    connect.execute(
                        'INSERT INTO Server (name, guid, url) VALUES (?, ?, ?)', (self.name, self.guid, self.url)
                    )

                # Иначе, обновляем
                else:
                    connect.execute('UPDATE Server SET name=?, url=?', (self.name, self.url))

                # TODO: аналогично заполнить команды: command_list

                connect.commit()

        from threading import Thread
        thread = Thread(target=_wait_server_running)
        thread.start()

    def all_exception_handler(self, status, message, traceback, version):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'

        error_text = traceback.strip().split('\n')[-1]
        error_text = error_text.split(':', maxsplit=1)[1].strip()
        print('[{}] Error: {}\n\n{}'.format(self.name, error_text, traceback))

        rs = self.generate_response(
            result=None,
            ok=False,
            error=error_text,
            traceback=traceback,
        )

        import json
        return json.dumps(rs)

    def run(self, port=0):
        # Set port
        cherrypy.config.update({'server.socket_port': port})

        # Autoreload off
        cherrypy.config.update({'engine.autoreload.on': False})

        try:
            cherrypy.quickstart(self)

        finally:
            print('Finish server "{}": port={}'.format(self.name, port))


if __name__ == '__main__':
    server = BaseServer()
    server.run(9090)
