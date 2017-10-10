#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG


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

    def _execute_body(self, command, command_name, **params):
        if DEBUG:
            result = 'COMMAND__EXCHANGE_RATE'
        else:
            # TODO: кэшировать команду -- пусть данные считаются "протухшими" через 6 часов
            from commands.command__exchange_rate import currency
            rate_list = currency.exchange_rate(['EUR', 'USD'])
            result = ', '.join(rate_list)

        rs = self.generate_response(result)
        if DEBUG:
            print('  rs[DEBUG]:', rs)
        else:
            print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = ExchangeRateServer()
    server.run()
