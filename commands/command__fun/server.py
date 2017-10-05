#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG


class FunServer(BaseServer):
    name = 'FunServer'
    guid = 'D24972621DAF4E35AA6BE68AB55BB46F'
    command_list = [
        Command(
            name='насмеши',
            uri='/execute',
            description='Случайная цитата башорга'
        ),
    ]

    def _execute_body(self, command, command_name, **params):
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
    server.run()
