#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer
from commands import DEBUG


class DamnServer(BaseServer):
    def __init__(self):
        super().__init__()

        self.name = 'DamnServer'
        self.guid = 'BD672810C4D8416FA0CE15B55487224D'

    def _execute_body(self, command):
        if not command:
            raise Exception("Неправильная команда 'ругнись': не указано на кого нужно ругнуться.")

        if DEBUG:
            result = command.upper()
        else:
            from commands.command__damn.damn import damn
            result = damn(command)

        ok = result is not None

        rs = self.generate_response(result, ok)
        if DEBUG:
            print('  rs[DEBUG]:', rs)
        else:
            print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = DamnServer()
    server.run(port=55001)
