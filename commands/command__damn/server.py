#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG


class DamnServer(BaseServer):
    name = 'DamnServer'
    guid = 'BD672810C4D8416FA0CE15B55487224D'
    command_list = [
        Command(
            name='ругнись',
            uri='/execute',
            description='Напиши кого бот отругает. Например: Бот, ругнись петр иваныч'
        ),
    ]

    def _execute_body(self, command, command_name, **params):
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
    server.run()
