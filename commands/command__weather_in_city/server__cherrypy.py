#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer
from commands import DEBUG


class WeatherServer(BaseServer):
    def __init__(self):
        super().__init__()

        self.name = 'WeatherServer'

    def _execute_body(self, rq=None):
        if 'command' not in rq:
            raise Exception("В запросе не найдено поле 'command'.")

        command = rq['command']
        if not command:
            raise Exception("Неправильная команда 'погода': не указан населенный пункт")

        if DEBUG:
            result = command.upper()
        else:
            from commands.command__weather_in_city.weather_in_city import get_weather
            result = get_weather(command)

        ok = result is not None

        rs = self.generate_response(result, ok)
        if DEBUG:
            print('  rs[DEBUG]:', rs)
        else:
            print('  rs:', rs)

        return rs

if __name__ == '__main__':
    server = WeatherServer()
    server.run(port=55003)
