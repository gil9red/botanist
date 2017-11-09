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


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/9a44a6bb0553769c2acc4550b587ff8864427f9f/mediawiki__wikipedia.py
def wiki_search(query: str, lang='ru', unquote_percent_encoded=False) -> str:
    # Default using wikipedia
    from mediawiki import MediaWiki
    wikipedia = MediaWiki(lang=lang)
    result = wikipedia.opensearch(query, results=1)
    if not result:
        return ''

    _, text, url = result[0]

    if unquote_percent_encoded:
        from urllib.parse import unquote
        url = unquote(url)

    return '{} ({})'.format(text, url)


from commands.base_server import BaseServer, Command


class WikipediaServer(BaseServer):
    name = 'WikipediaServer'
    guid = '594BCE0A8E2D4CA2B8840DFCDCCF8BB9'
    command_list = [
        Command(
            name='wiki',
            uri='/execute',
            description='Команда для поиска информации на русской википедии. Например: Бот, wiki металлика',
            priority=7,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception(
                "Неправильная команда '{}': нужно указать выражение, например: металлика".format(command_name)
            )

        # В сообщении ссылки с кирилицей лучше будут смотреться чем percent-encoded
        result = wiki_search(command, unquote_percent_encoded=True)
        print('"{}" -> {}'.format(command, result))

        text = result.strip()
        if not text:
            return '<Нет результатов>'

        return self.generate_response(result=text)


if __name__ == '__main__':
    server = WikipediaServer()
    server.run()
