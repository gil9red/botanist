#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import typing
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

        rs = self.generate_response(result=result)
        return rs


if __name__ == '__main__':
    server = FunServer()
    server.run()
