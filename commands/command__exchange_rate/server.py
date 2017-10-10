#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
from commands.base_server import BaseServer, Command


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

    def _execute_body(self, command, command_name, **params):
        # TODO: кэшировать команду -- пусть данные считаются "протухшими" через 6 часов
        from commands.command__exchange_rate import currency
        rate_list = currency.exchange_rate(['EUR', 'USD'])
        result = ', '.join(rate_list)

        rs = self.generate_response(result)
        return rs


if __name__ == '__main__':
    server = ExchangeRateServer()
    server.run()
