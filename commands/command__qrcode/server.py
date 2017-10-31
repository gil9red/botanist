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


import common
from commands.base_server import BaseServer, Command


class QRCodeServer(BaseServer):
    name = 'QRCodeServer'
    guid = '60BC4D9FB8BB461E996E0F22C37F7498'
    command_list = [
        Command(
            name='qrcode',
            uri='/execute',
            description='Команда для генерации QR Code. Например: Бот, qrcode Привет мир!. '
                        'Или: Бот, qrcode https://github.com/gil9red',
            priority=9,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception("Неправильная команда 'qrcode': нужно указать текст, например: Привет мир!")

        # https://github.com/gil9red/SimplePyScripts/blob/d3ee62b48dd1277aa68244f7ec2966183517b931/generate_qrcode/main.py
        import qrcode
        img = qrcode.make(command)

        extension = 'png'

        # In memory
        import io
        io_data = io.BytesIO()
        img.save(io_data, extension)

        attachment = common.FileAttachment(content=io_data.getvalue(), extension=extension)

        return self.generate_response(attachment=attachment, attachment_type=common.AttachmentType.IMAGE)


if __name__ == '__main__':
    server = QRCodeServer()
    server.run()
