#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.base_server import BaseServer, Command
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
            name='тест несколько картинок',
            uri='/execute?' + common.TYPE_LIST_IMAGE,
            description='Возвращает несколько тестовых картинок',
        ),
        Command(
            name='тест дай гифку',
            uri='/execute?' + common.TYPE_GIF,
            description='Возвращает тестовую гифку',
        ),
    ]

    def _execute_body(self, command, command_name, **params):
        function_list = list(params.keys())
        func_name = function_list[0]

        import pathlib
        current_dir = pathlib.Path(__file__).parent

        if func_name == common.TYPE_IMAGE:
            with open(current_dir / 'Jimm Kerry.jpg', mode='rb') as f:
                result = f.read()

        elif func_name == common.TYPE_GIF:
            with open(current_dir / 'Jimm Kerry.gif', mode='rb') as f:
                result = f.read()

        elif func_name == common.TYPE_LIST_IMAGE:
            result = []

            import glob
            for file_name in glob.glob(current_dir / 'images/*.jpg'):
                with open(file_name, mode='rb') as f:
                    result.append(f.read())

        else:
            message = "Неправильная команда '{}': не найдена функция '{}', доступны следующие функции: {}"
            message = message.format(
                command_name,
                func_name,
                ', '.join([common.TYPE_IMAGE, common.TYPE_GIF, common.TYPE_LIST_IMAGE])
            )
            raise Exception(message)

        rs = self.generate_response(result, data_type=func_name)
        return rs


if __name__ == '__main__':
    server = TestAttachmentServer()
    server.run()
