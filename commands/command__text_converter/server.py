#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG
from commands.command__text_converter.hex2str import hex2str, str2hex
from commands.command__text_converter.bin2str import bin2str, str2bin


class TextConverter(BaseServer):
    name = 'TextConverter'
    guid = '531B994DED974F1586BA370F0AE1BE14'
    command_list = [
        Command(
            name='str2hex',
            uri='/execute?str2hex',
            description='Конвертация строки в HEX. Например: Бот, str2hex Привет!'
        ),
        Command(
            name='hex2str',
            uri='/execute?hex2str',
            description='Конвертация из HEX в строку. Например: Бот, hex2str CFF0E8E2E5F221'
        ),

        Command(
            name='str2bin',
            uri='/execute?str2bin',
            description='Конвертация из текстовой строки в бинарную. Например: Бот, str2bin Привет!'
        ),
        Command(
            name='bin2str',
            uri='/execute?bin2str',
            description='Конвертация из бинарной строки в текстовую. Например: Бот, bin2str 11001111 11110000 '
                        '11101000 11100010 11100101 11110010 00100001'
        ),
    ]

    name_by_func = {
        'hex2str': hex2str,
        'str2hex': str2hex,
        'bin2str': bin2str,
        'str2bin': str2bin,
    }

    def _execute_body(self, command, command_name, **params):
        if DEBUG:
            result = command.upper()
            rs = self.generate_response(result, ok=True)
            if DEBUG:
                print('  rs[DEBUG]:', rs)
            else:
                print('  rs:', rs)

            return rs

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

            raise Exception('При выполнении команды "{}" произошла ошибка "{}". '
                            'Проверь что данные правильные.'.format(command_name, e))

        ok = result is not None

        rs = self.generate_response(result, ok)
        print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = TextConverter()
    server.run()
