#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import typing

from commands.base_server import BaseServer, Command
import common


class TestAttachmentServer(BaseServer):
    name = 'TestAttachmentServer'
    guid = 'D2EA28FA35D244E5A36EECC5FA3EA759'
    command_list = [
        Command(
            name='тест дай картинку',
            uri='/execute?' + common.TYPE_IMAGE,
            description='Возвращает тестовую картинку',
        ),
        Command(
            name='тест несколько картинок',
            uri='/execute?' + common.TYPE_LIST_IMAGE,
            description='Возвращает несколько тестовых картинок',
        ),
        Command(
            name='тест дай гифку',
            uri='/execute?' + common.TYPE_GIF,
            description='Возвращает тестовую гифку',
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        function_list = list(params.keys())
        func_name = function_list[0]

        import pathlib
        current_dir = pathlib.Path(__file__).parent

        result = None

        if func_name == common.TYPE_IMAGE:
            file = current_dir / 'Jimm Kerry.jpg'
            result = 'Jimm Kerry.jpg'
            attachment = file.read_bytes()

        elif func_name == common.TYPE_GIF:
            file = current_dir / 'Jimm Kerry.gif'
            result = 'Jimm Kerry.gif'
            attachment = file.read_bytes()

        elif func_name == common.TYPE_LIST_IMAGE:
            attachment = [file.read_bytes() for file in current_dir.glob('images/*.jpg')]

        else:
            message = "Неправильная команда '{}': не найдена функция '{}', доступны следующие функции: {}"
            message = message.format(
                command_name,
                func_name,
                ', '.join([common.TYPE_IMAGE, common.TYPE_GIF, common.TYPE_LIST_IMAGE])
            )
            raise Exception(message)

        rs = self.generate_response(result=result, attachment=attachment, data_type=func_name)
        return rs


if __name__ == '__main__':
    server = TestAttachmentServer()
    server.run()
