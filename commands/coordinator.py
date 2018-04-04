#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
import sys
import typing

current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)


from commands.base_server import BaseServer, Command
from common import generate_request
import db

# TODO: интересная идея реализации конвеера команд, например: str2hex -> str2base64 -> qrcode
#       т.е. в координатор попадает текст, который преобразуется в HEX, HEX преобразуется в base64, а BASE64
#       преобразуется в картинку QRCode


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/460f3538ebc0fb78628ea885ac7d39481404fa1e/Damerau%E2%80%93Levenshtein_distance__misprints__%D0%BE%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%BA%D0%B8/use__pyxdameraulevenshtein/fix_command.py
def fix_command(text, all_commands):
    try:
        import numpy as np
        array = np.array(all_commands)

        # Использование алгоритма "Расстояние Дамерау — Левенштейна"
        from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance_ndarray
        result = list(zip(all_commands, list(normalized_damerau_levenshtein_distance_ndarray(text, array))))
        # print('\n' + text, sorted(result, key=lambda x: x[1]))

        command, rate = min(result, key=lambda x: x[1])

        # Подобранное значение для определения совпадения текста среди значений указанного списка
        # Если True, считаем что слишком много ошибок в слове, т.е. text среди all_commands нет
        if rate >= 0.3:
            return text

        return command

    except Exception as e:
        import traceback
        print('Error: {}\n\n{}'.format(e, traceback.format_exc()))

        return text


class CoordinatorServer(BaseServer):
    name = 'CoordinatorServer'
    guid = 'B57B73C8F8D442C48EDAFC951963D7A5'
    command_list = [
        Command(
            name='команды',
            uri='/execute',
            description='Возвращает топ10 команд',
            priority=999
        ),
        Command(
            name='все команды',
            uri='/execute',
            description='Возвращает все команды',
            priority=998
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    @BaseServer.expose
    @BaseServer.json_out
    def get_commands(self, as_result=None, max_number=None) -> dict:
        print(self.request.params)

        all_command_name_by_description = db.get_all_command_name_by_description()

        if as_result is not None:
            items = list(all_command_name_by_description.items())[:max_number]
            result = '\n'.join('✓ {}: {}'.format(k, v) for k, v in items)

            return self.generate_response(result=result)

        return all_command_name_by_description

    @BaseServer.expose
    @BaseServer.json_out
    def get_top10_commands(self, as_result=None) -> dict:
        return self.get_commands(as_result, max_number=10)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        # Если команды нет, показываем список команд
        if not command.strip():
            return self.get_top10_commands(as_result=True)

        # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
        execute_command = command.lower()
        print('execute_command: "{}"'.format(execute_command))

        all_command_by_url = db.get_all_command_name_by_url()
        command_name_list = [x.lower() for x in all_command_by_url.keys()]

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

                return result

        # Обработка собственных команд
        if execute_command == 'команды':
            return self.get_top10_commands(as_result=True)

        elif execute_command == 'все команды':
            return self.get_commands(as_result=True)

        for command_name, url in all_command_by_url.items():
            if execute_command.startswith(command_name.lower()):
                command_text = command[len(command_name):].strip()
                print('Found server: {}, command name: "{}", command text: "{}"'.format(
                    url, command_name, command_text)
                )

                rq = generate_request(command_name, command_text)
                print('Generate request:', rq)

                import requests
                try:
                    rs = requests.post(url, json=rq)
                    print('Response:', rs.text)
                    return rs.json()

                except requests.exceptions.ConnectionError:
                    error = 'Сервер команды "{}" ({}) недоступен'.format(command_name, url)
                    return self.generate_response(error=error)

        error = 'Что-то пошло не так: команда "{}" не была распознана'.format(command)
        return self.generate_response(error=error)

    def _before_run(self):
        def _thread_func():
            import time
            import db
            import requests

            # Немного дадим времени серверам перед проверкой (особенно http-серверу самого координатора)
            time.sleep(2)

            while True:
                for server in db.get_all_server():
                    name = server['name']
                    guid = server['guid']
                    url = server['url']

                    try:
                        requests.get(url, timeout=0.1)
                        availability = True

                    except requests.exceptions.ConnectionError:
                        availability = False

                    # TODO: лучше это логировать в отдельный файл, т.к. логировать
                    #       будет много и часто и общий лог засорять не нужно
                    print('name: "{}", availability={}'.format(name, availability))
                    db.update_availability(guid, availability)

                print('\n')

                # Иначе может не вывести сразу в консоль
                sys.stdout.flush()

                time.sleep(25)

        from threading import Thread
        thread = Thread(target=_thread_func)
        thread.start()


if __name__ == '__main__':
    server = CoordinatorServer()
    server.run()
