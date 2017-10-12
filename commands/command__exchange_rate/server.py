#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta
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
from commands.command__exchange_rate import currency


class ExchangeRateServer(BaseServer):
    name = 'ExchangeRateServer'
    guid = '21535ECEF2104BFD8F1CD1DC715309AA'
    command_list = [
        Command(
            name='курс валют',
            uri='/execute',
            description='Показать текущий курс евро и доллара',
            priority=9,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def __init__(self):
        super().__init__()

        # Поле для сохранения результата
        self.last_result = None

        # Поле для сохранения времени последнего запроса
        self.last_request_time = None

        # Поле для сохранения времени, когда кэш испортится
        self.cache_update_time = None

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        delta = timedelta(hours=1)

        if self.last_request_time is None or self.cache_update_time < datetime.now():
            rate_list = currency.exchange_rate(['EUR', 'USD'])
            self.last_result = ', '.join(rate_list)
            self.last_request_time = datetime.now()
            self.cache_update_time = self.last_request_time + delta

            print('Обновляю кэшированный курс валют: "{}", кэш испортится ''в {}.'
                  .format(self.last_result, self.cache_update_time))

        else:
            print('Возвращаю кэш за {}, обновление кэша будет через {} в {}'
                  .format(self.last_request_time, self.cache_update_time - datetime.now(), self.cache_update_time))

        return self.last_result


if __name__ == '__main__':
    server = ExchangeRateServer()
    server.run()
