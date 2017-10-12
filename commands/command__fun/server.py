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


class FunServer(BaseServer):
    name = 'FunServer'
    guid = 'D24972621DAF4E35AA6BE68AB55BB46F'
    command_list = [
        Command(
            name='насмеши',
            uri='/execute',
            description='Случайная цитата башорга',
            priority=10,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        from commands.command__fun.fun import get_random_quote
        result = get_random_quote()

        return result


if __name__ == '__main__':
    server = FunServer()
    server.run()
