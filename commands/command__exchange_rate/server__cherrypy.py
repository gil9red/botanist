#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer
from commands import DEBUG


class ExchangeRateServer(BaseServer):
    def __init__(self):
        super().__init__()

        self.name = 'ExchangeRateServer'

    def _execute_body(self, command):
        if DEBUG:
            result = 'COMMAND__EXCHANGE_RATE'
        else:
            from commands.command__exchange_rate import currency
            rate_list = currency.exchange_rate(['EUR', 'USD'])
            result = ', '.join(rate_list)

        ok = result is not None

        rs = self.generate_response(result, ok)
        if DEBUG:
            print('  rs[DEBUG]:', rs)
        else:
            print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = ExchangeRateServer()
    server.run(port=55004)
