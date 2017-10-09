#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
from commands import DEBUG
import common


class TestAttachmentServer(BaseServer):
    name = 'TestAttachmentServer'
    guid = 'D2EA28FA35D244E5A36EECC5FA3EA759'
    command_list = [
        Command(
            name='тест дай картинку',
            uri='/execute?' + common.TYPE_IMAGE,
            description='Возвращает тестовую картинку',
        ),
        Command(
            name='тест дай гифку',
            uri='/execute?' + common.TYPE_GIF,
            description='Возвращает тестовую гифку',
        ),
    ]

    def _execute_body(self, command, command_name, **params):
        if DEBUG:
            result = command.upper()
            rs = self.generate_response(result, ok=True)
            if DEBUG:
                print('  rs[DEBUG]:', rs)
            else:
                print('  rs:', rs)

            return rs

        function_list = list(params.keys())
        func_name = function_list[0]

        if func_name == common.TYPE_IMAGE:
            with open('Jimm Kerry.jpg', mode='rb') as f:
                result = f.read()

        elif func_name == common.TYPE_GIF:
            with open('Jimm Kerry.gif', mode='rb') as f:
                result = f.read()

        else:
            message = "Неправильная команда '{}': не найдена функция '{}', доступны следующие функции: {}"
            message = message.format(
                command_name,
                func_name,
                ', '.join([common.TYPE_IMAGE, common.TYPE_GIF])
            )
            raise Exception(message)

        rs = self.generate_response(result, ok=True, data_type=func_name)
        print('  rs:', rs)

        return rs


if __name__ == '__main__':
    server = TestAttachmentServer()
    server.run()
