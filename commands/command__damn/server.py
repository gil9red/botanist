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


class DamnServer(BaseServer):
    name = 'DamnServer'
    guid = 'BD672810C4D8416FA0CE15B55487224D'
    command_list = [
        Command(
            name='ругнись',
            uri='/execute',
            description='Напиши кого бот отругает. Например: Бот, ругнись петр иваныч',
            priority=7,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, rq: dict, **params: dict) -> typing.Union[dict, str]:
        command = rq['command']
        command_name = rq['command_name']

        if not command:
            raise Exception("Неправильная команда 'ругнись': не указано на кого нужно ругнуться.")

        from commands.command__damn.damn import damn
        result = damn(command)

        return result


if __name__ == '__main__':
    server = DamnServer()
    server.run()
