#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG


class WeatherServer(BaseServer):
    name = 'WeatherServer'
    guid = 'EF3D2E05CBAA49F2867C742EA7D856D0'
    command_list = [
        Command(
            name='погода',
            uri='/execute',
            description='Погода в указанном населенном пункте. Например: Бот, погода магнитогорск',
            priority=10,
        ),
    ]

    def _execute_body(self, command, command_name, **params):
        if not command:
            raise Exception("Неправильная команда 'погода': не указан населенный пункт")

        if DEBUG:
            result = command.upper()
        else:
            from commands.command__weather_in_city.weather_in_city import get_weather
            result = get_weather(command)

        rs = self.generate_response(result)
        if DEBUG:
            print('  rs[DEBUG]:', rs)
        else:
            print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = WeatherServer()
    server.run()
