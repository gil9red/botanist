#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time

from collections import namedtuple
Command = namedtuple('Command', ['name', 'uri', 'description', 'priority'])
Command.__new__.__defaults__ = (None, None, None, 0)

import common
common.make_backslashreplace_console()

# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


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

        self.last_elapsed = None

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
    def execute(self, **params):
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
            rs = self._execute_body(command, command_name, **params)

        finally:
            self.last_elapsed = time.clock() - start_elapsed
            print('  Elapsed time: {:.7f} secs'.format(self.last_elapsed))

        if type(rs) == str:
            rs = self.generate_response(
                result=rs,
                ok=True,
            )

        rs['elapsed'] = self.last_elapsed

        print('[{}] Response: {}'.format(self.name, rs))
        return rs

    def _execute_body(self, command, command_name, **params):
        raise Exception('_execute_body is not implemented!')

    def generate_response(self, result=None, ok=True, error=None, traceback=None,
                          elapsed=None, data_type=common.TYPE_TEXT):
        # TODO: Завести метод кодирования сообщения в зависимости от data_type
        #       типа: create_message_from_data_type / get_message_from_data_type
        if type(result) == bytes and data_type in [common.TYPE_IMAGE, common.TYPE_GIF]:
            import base64
            result = base64.b64encode(result).decode('utf-8')

        from collections import OrderedDict
        rs = OrderedDict()
        rs['result'] = result
        rs['ok'] = ok
        rs['type'] = data_type
        rs['error'] = error
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

            print('Start server "{}": {}:{} / {}'.format(self.name, self.host, self.port, self.url))
            print('Commands ({}):'.format(len(self.command_list)))
            for command in self.command_list:
                print('    {}'.format(command))

            import db
            db.fill_server_info(self)

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
            elapsed=self.last_elapsed,
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
    server.run()
