#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer
from commands import DEBUG


class FunServer(BaseServer):
    def __init__(self):
        super().__init__()

        self.name = 'FunServer'

    def _execute_body(self, command):
        if DEBUG:
            result = 'COMMAND__FUN'
        else:
            from commands.command__fun.fun import get_random_quote
            result = get_random_quote()

        ok = result is not None

        rs = self.generate_response(result, ok)
        if DEBUG:
            print('  rs[DEBUG]:', rs)
        else:
            print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = FunServer()
    server.run(port=55002)
