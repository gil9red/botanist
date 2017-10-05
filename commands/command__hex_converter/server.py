#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG
from commands.command__hex_converter.hex2str import hex2str, str2hex


class HexConverter(BaseServer):
    name = 'HexConverter'
    guid = '531B994DED974F1586BA370F0AE1BE14'
    command_list = [
        Command(
            name='str2hex',
            uri='/execute?str2hex',
            description='Конвертация строки в HEX'
        ),
        Command(
            name='hex2str',
            uri='/execute?hex2str',
            description='Конвертация из HEX в строку'
        ),
    ]

    def _execute_body(self, command, command_name, **params):
        if DEBUG:
            result = command.upper()
            rs = self.generate_response(result, ok=True)
            if DEBUG:
                print('  rs[DEBUG]:', rs)
            else:
                print('  rs:', rs)

            return rs

        if not command:
            raise Exception("Неправильная команда '{}': не указан текст".format(command_name))

        result = None

        if 'hex2str' in params:
            result = hex2str(command)

        elif 'str2hex' in params:
            result = str2hex(command)

        ok = result is not None

        rs = self.generate_response(result, ok)
        print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = HexConverter()
    server.run()
