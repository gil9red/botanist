#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: использовать jsonschema для проверки запросов API
import typing
import sys


# Если True, тогда модули-команды вместо выполнения своей команды вернут эхо в верхнем регистре
DEBUG = False
# DEBUG = True

# TODO: для logging.basicConfig определить filename для сбора всякие логов (проверить
#       как сработает для уже установленых логов)
# cherrypy.config.update({
#     # Для каждого сервера можно реализовать:
#     # Дополнительно можно к имени лога добавлять имя сервера и путь указывать полный, в корень проекта в папке logs
#     # Например: mini_vk_bot/logs
#     'log.access_file': "access.log",
#     'log.error_file': "error.log",
# })


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)


if __name__ == '__main__':
    import common
    rs = common.execute('команды')
    print(rs)

    file_name = 'command__get_image_info/example.jpg'
    with open(file_name, 'rb') as f:
        content = f.read()
        extension = pathlib.Path(file_name).suffix[1:]

    file_attachment = common.FileAttachment(content=content, extension=extension)
    attachment_type = common.AttachmentType.IMAGE
    attachment = common.create_attachment(file_attachment, attachment_type)
    rs = common.execute('получить информацию о картинке', attachment)
    print(rs)
