#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import (
    generate_request,
    ALL_COMMAND_BY_URL,
    ALL_COMMAND_NAME_BY_DESCRIPTION,
)

# TODO: поддержать флаг DEBUG_ALONE_COORDINATOR


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/460f3538ebc0fb78628ea885ac7d39481404fa1e/Damerau%E2%80%93Levenshtein_distance__misprints__%D0%BE%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%BA%D0%B8/use__pyxdameraulevenshtein/fix_command.py
def fix_command(text, all_commands):
    import numpy as np
    array = np.array(all_commands)

    # Использование алгоритма "Расстояние Дамерау — Левенштейна"
    from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance_ndarray
    result = list(zip(all_commands, list(normalized_damerau_levenshtein_distance_ndarray(text, array))))
    # print('\n' + text, sorted(result, key=lambda x: x[1]))

    command, rate = min(result, key=lambda x: x[1])

    # Подобранное значение для определения совпадения текста среди значений указанного списка
    if rate >= 0.3:
        return text

    return command


class CoordinatorServer(BaseServer):
    name = 'CoordinatorServer'
    guid = 'B57B73C8F8D442C48EDAFC951963D7A5'
    command_list = [
         Command(
             name='команды',
             uri='/execute',
             description='Показать список команд'
         ),
    ]

    @BaseServer.expose
    @BaseServer.json_out
    def get_commands(self, as_result=None):
        print(self.request.params)

        if as_result is not None:
            result = '\n'.join(
                '✓ {}: {}'.format(k, v) for k, v in sorted(ALL_COMMAND_NAME_BY_DESCRIPTION.items(), key=lambda x: x[0])
            )

            rs = self.generate_response(result, ok=True)
            return rs

        return ALL_COMMAND_NAME_BY_DESCRIPTION

    def _execute_body(self, command):
        print('Execute command: "{}"'.format(command))

        # Если команды нет, показываем список команд
        if not command.strip():
            return self.get_commands(as_result=True)

        # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
        execute_command = command.lower()
        print('execute_command: "{}"'.format(execute_command))

        command_name_list = list(ALL_COMMAND_BY_URL.keys())

        # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки,
        # пытаемся найти, учитывая, что в ней могут быть опечатки, иначе ругаемся на неизвестную команду
        if not any(execute_command.startswith(x) for x in command_name_list):
            fix_execute_command = None

            for command_name in command_name_list:
                word_list = execute_command.split()
                for i in range(1, len(word_list) + 1):
                    part_command_name = ' '.join(word_list[:i])

                    # Если нашли команду
                    if command_name == fix_command(part_command_name, command_name_list):
                        # Составляем команду с текстом
                        fix_execute_command = ' '.join([command_name] + word_list[i:])

            # Если это была опечатка, обновляем запрос команды, исправив опечатку
            if fix_execute_command is not None and execute_command != fix_execute_command:
                print('fix execute command: "{}" -> "{}"'.format(execute_command, fix_execute_command))
                execute_command = fix_execute_command

            # Если не удалось разобрать команду как опечатку
            if fix_execute_command is None:
                result = 'Получена неизвестная команда "{}".\n' \
                         'Чтобы узнать доступные команды введи: Бот, команды'.format(command)

                rs = self.generate_response(result, ok=True)
                print('  rs:', rs)

                return rs

        # Обработка собственной команды
        if execute_command == 'команды':
            return self.get_commands(as_result=True)

        for command_name, url in ALL_COMMAND_BY_URL.items():
            if execute_command.startswith(command_name.lower()):
                command_text = command[len(command_name):].strip()
                print('Found server: {}, command name: "{}", command text: "{}"'.format(
                    url, command_name, command_text)
                )

                import requests
                try:
                    rs = requests.post(url, json=generate_request(command_text))
                    return rs.json()

                except requests.exceptions.ConnectionError:
                    error = 'Сервер команды "{}" ({}) недоступен'.format(command_name, url)

                    rs = self.generate_response(result=None, ok=False, error=error)
                    return rs

        error = 'Что-то пошло не так: команда "{}" не была распознана'.format(command)
        rs = self.generate_response(result=None, ok=False, error=error)
        return rs


if __name__ == '__main__':
    server = CoordinatorServer()
    server.run(port=55000)
