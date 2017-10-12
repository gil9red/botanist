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
from commands.command__text_converter.hex2str import hex2str, str2hex
from commands.command__text_converter.bin2str import bin2str, str2bin


class TextConverter(BaseServer):
    name = 'TextConverter'
    guid = '531B994DED974F1586BA370F0AE1BE14'
    command_list = [
        Command(
            name='str2hex',
            uri='/execute?str2hex',
            description='Конвертация строки в HEX. Например: Бот, str2hex Привет!',
            priority=6,
        ),
        Command(
            name='hex2str',
            uri='/execute?hex2str',
            description='Конвертация из HEX в строку. Например: Бот, hex2str CFF0E8E2E5F221',
            priority=6,
        ),

        Command(
            name='str2bin',
            uri='/execute?str2bin',
            description='Конвертация из текстовой строки в бинарную. Например: Бот, str2bin Привет!',
            priority=5,
        ),
        Command(
            name='bin2str',
            uri='/execute?bin2str',
            description='Конвертация из бинарной строки в текстовую. Например: Бот, bin2str 11001111 11110000 '
                        '11101000 11100010 11100101 11110010 00100001',
            priority=5,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    name_by_func = {
        'hex2str': hex2str,
        'str2hex': str2hex,
        'bin2str': bin2str,
        'str2bin': str2bin,
    }

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception("Неправильная команда '{}': не указан текст".format(command_name))

        function_list = list(params.keys())
        if not function_list:
            raise Exception("Неправильная команда '{}': не указана вызываемая функция, "
                            "например 'hex2str'".format(command_name))

        func_name = function_list[0]

        if func_name not in self.name_by_func:
            raise Exception("Неправильная команда '{}': не найдена функция '{}', доступны следующие "
                            "функции: {}".format(command_name, func_name, ', '.join(self.name_by_func.keys())))

        try:
            # Вызов функции по ее имени
            result = self.name_by_func[func_name](command)

        except Exception as e:
            import traceback
            print('Error: {}\n\n{}'.format(e, traceback.format_exc()))

            raise Exception('При выполнении команды "{}" произошла ошибка. '
                            'Проверь что данные правильные. Текст ошибки: "{}".'.format(command_name, e))

        return result


if __name__ == '__main__':
    server = TextConverter()
    server.run()
