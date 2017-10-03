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

    def __init__(self):
        # Set a custom response for errors.
        self._cp_config = {'error_page.default': self.all_exception_handler}

        self.name = 'BaseServer'

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {
            'name': self.name
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

        rs = self._execute_body(rq)
        print('[{}] Response: {}'.format(self.name, rs))

        if type(rs) == str:
            rs = self.generate_response(
                result=rs,
                ok=True,
            )

        return rs

    def _execute_body(self, rq):
        raise Exception('_execute_body is not implemented!')

    def generate_response(self, result=None, ok=True, error=None, traceback=None):
        from collections import OrderedDict
        rs = OrderedDict()
        rs['result'] = result
        rs['ok'] = ok
        rs['error'] = error
        rs['traceback'] = traceback
        rs['server_name'] = self.name

        return rs

    def all_exception_handler(self, status, message, traceback, version):
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'

        error_text = traceback.strip().split('\n')[-1]
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

        cherrypy.quickstart(self)


if __name__ == '__main__':
    server = BaseServer()
    server.run(port=9090)
