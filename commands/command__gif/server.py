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


class GifServer(BaseServer):
    name = 'GifServer'
    guid = '0CBBE285D35D4BCCB28EF3554CD3D4DC'
    command_list = [
        Command(
            # TODO: если не указан запрос, возвращать случайную гифку
            name='gif',
            uri='/execute',
            description='Возвращает по запросу гифку. Например: Бот, gif котята',
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception(
                "Неправильная команда '{}': нужно указать текст, например: котята".format(command_name)
            )

        import giphy
        url = giphy.get_gif(command)
        if not url:
            return '<Не удалось найти гифку>'

        import requests
        rs = requests.get(url)

        import common
        attachment = common.FileAttachment(content=rs.content, extension='gif')
        attachment_type = common.AttachmentType.GIF

        return self.generate_response(attachment=attachment, attachment_type=attachment_type)


if __name__ == '__main__':
    server = GifServer()
    server.run()
