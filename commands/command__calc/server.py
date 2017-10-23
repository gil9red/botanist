#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import typing
import sys


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())
dir_up_up = str(current_dir.parent.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)

if dir_up_up not in sys.path:
    sys.path.append(dir_up_up)


from commands.base_server import BaseServer, Command


class CalcServer(BaseServer):
    name = 'CalcServer'
    guid = '9A306C919E0941C68D92F190E3F89C2B'
    command_list = [
        Command(
            name='калькулятор',
            uri='/execute',
            description='Погода в указанном населенном пункте. Например: Бот, калькулятор 2 + 2 * 2 или '
                        'Бот, калькулятор (0xFF + 255) / 0b1010',
            priority=9,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception("Неправильная команда 'калькулятор': нужно указать выражение, например: 2 + 2 * 2")

        # Калькулятор из: https://github.com/gil9red/SimplePyScripts/blob/master/calculator/use_numexpr_module/main.py
        import numexpr
        result = str(numexpr.evaluate(command))

        return result


if __name__ == '__main__':
    server = CalcServer()
    server.run()
