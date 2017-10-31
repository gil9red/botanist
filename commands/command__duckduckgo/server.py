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


class DuckDuckGoServer(BaseServer):
    name = 'DuckDuckGoServer'
    guid = 'F7C3D7520D434C82A28B48967F5513B6'
    command_list = [
        Command(
            name='ddg',
            uri='/execute',
            description='Команда для поиска информации, используя api duckduckgo. Например: Бот, ddg металлика',
            priority=7,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception("Неправильная команда 'найти': нужно указать выражение, например: металлика")

        from commands.command__duckduckgo import duckduckgo
        query_result = duckduckgo.query(command, kad='ru_RU')
        print('"{}" -> {}'.format(command, query_result.json))

        if not query_result.results:
            return duckduckgo.get_zci(command, on_no_results='<Нет результатов>', kad='ru_RU')

        attachment = None
        attachment_type = None

        img_url = query_result.image.url
        if img_url:
            try:
                import requests
                rs = requests.get(img_url)

                content = rs.content
                extension = pathlib.Path(img_url).suffix[1:]

                attachment = common.FileAttachment(content=content, extension=extension)
                attachment_type = common.AttachmentType.IMAGE

            except:
                pass

        text = query_result.abstract.text.strip()

        url = query_result.abstract.url
        if url:
            from urllib.parse import unquote
            url = unquote(url)
            text += ' (' + url + ')'

        text = text.strip()

        rs = self.generate_response(result=text, attachment=attachment, attachment_type=attachment_type)
        return rs


if __name__ == '__main__':
    server = DuckDuckGoServer()
    server.run()
