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
import common


class TestAttachmentServer(BaseServer):
    name = 'TestAttachmentServer'
    guid = 'D2EA28FA35D244E5A36EECC5FA3EA759'
    command_list = [
        Command(
            name='тест картинку',
            uri='/execute?' + common.TYPE_IMAGE,
            description='Возвращает тестовую картинку. Например: Бот, тест картинку',
        ),
        Command(
            name='тест много картинок',
            uri='/execute?' + common.TYPE_LIST_IMAGE,
            description='Возвращает несколько тестовых картинок. Например: Бот, тест много картинок',
        ),
        Command(
            name='тест гифку',
            uri='/execute?' + common.TYPE_GIF,
            description='Возвращает тестовую гифку. Например: Бот, тест гифку',
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
            result = file.name  # 'Jimm Kerry.jpg'
            extension = file.suffix[1:]
            content = file.read_bytes()

            attachment = common.FileAttachment(extension=extension, content=content)

        elif func_name == common.TYPE_GIF:
            file = current_dir / 'Jimm Kerry.gif'
            result = 'Jimm Kerry.gif'
            extension = file.suffix[1:]
            content = file.read_bytes()

            attachment = common.FileAttachment(extension=extension, content=content)

        elif func_name == common.TYPE_LIST_IMAGE:
            attachment = []

            for file in current_dir.glob('images/*.jpg'):
                extension = file.suffix[1:]
                content = file.read_bytes()

                file_attachment = common.FileAttachment(extension=extension, content=content)
                attachment.append(file_attachment)

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
