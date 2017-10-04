#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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

    def __init__(self):
        # Set a custom response for errors.
        self._cp_config = {'error_page.default': self.all_exception_handler}

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

    def run(self, port=9090):
        # Set port
        cherrypy.config.update({'server.socket_port': port})

        # Autoreload off
        cherrypy.config.update({'engine.autoreload.on': False})

        print('Start server "{}": port={}'.format(self.name, port))
        try:
            cherrypy.quickstart(self)

        finally:
            print('Finish server "{}": port={}'.format(self.name, port))


if __name__ == '__main__':
    server = BaseServer()
    server.run(port=9090)
