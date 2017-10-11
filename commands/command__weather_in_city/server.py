#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import typing

from commands.base_server import BaseServer, Command


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

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, command: str, command_name: str, **params: dict) -> typing.Union[dict, str]:
        if not command:
            raise Exception("Неправильная команда 'погода': не указан населенный пункт")

        from commands.command__weather_in_city.weather_in_city import get_weather
        result = get_weather(command)

        return result


if __name__ == '__main__':
    server = WeatherServer()
    server.run()
