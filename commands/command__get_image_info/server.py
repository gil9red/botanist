#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/print_exif/main.py
def get_exif_tags(file_object_or_file_name, as_category=True):
    if type(file_object_or_file_name) == str:
        # Open image file for reading (binary mode)
        file_object_or_file_name = open(file_object_or_file_name, mode='rb')

    # Return Exif tags
    # pip install exifread
    import exifread
    tags = exifread.process_file(file_object_or_file_name)
    tags_by_value = dict()

    if not tags:
        # print('Not tags')
        return tags_by_value

    # print('Tags ({}):'.format(len(tags)))

    for tag, value in tags.items():
        # Process value
        try:
            if value.field_type == 1:
                try:
                    # If last 2 items equals [0, 0]
                    if value.values[-2:] == [0, 0]:
                        value = bytes(value.values[:-2]).decode('utf-16')
                    else:
                        value = bytes(value.values).decode('utf-16')

                except:
                    value = str(value.values)
            else:
                value = value.printable

            value = value.strip()

        except:
            # Example tag JPEGThumbnail
            if type(value) == bytes:
                import base64
                value = base64.b64encode(value).decode()

        # print('  "{}": {}'.format(tag, value))

        if not as_category:
            tags_by_value[tag] = value

        else:
            # Fill categories_by_tag
            if ' ' in tag:
                category, sub_tag = tag.split(' ', maxsplit=1)

                if category not in tags_by_value:
                    tags_by_value[category] = dict()

                tags_by_value[category][sub_tag] = value

            else:
                tags_by_value[tag] = value

    # print()

    return tags_by_value


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/human_byte_size.py
def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/84651cfefaee768851170ec4ba7d025bbaae622d/get_image_info/main.py#L84
def get_image_info(file_name__or__bytes__or__bytes_io, pretty_json_str=False):
    data = file_name__or__bytes__or__bytes_io
    type_data = type(data)

    # File name
    if type_data == str:
        with open(data, mode='rb') as f:
            data = f.read()

    if type(data) == bytes:
        import io
        data = io.BytesIO(data)

    length = len(data.getvalue())
    exif = get_exif_tags(data)

    from PIL import Image
    img = Image.open(data)

    # Save order
    from collections import OrderedDict
    info = OrderedDict()
    info['length'] = OrderedDict()
    info['length']['value'] = length
    info['length']['text'] = sizeof_fmt(length)

    info['format'] = img.format
    info['mode'] = img.mode
    info['channels'] = len(img.getbands())
    info['bit_color'] = {
        '1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32,
        'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32
    }[img.mode]

    info['size'] = OrderedDict()
    info['size']['width'] = img.width
    info['size']['height'] = img.height

    info['exif'] = exif

    if pretty_json_str:
        import json
        info = json.dumps(info, indent=4, ensure_ascii=False)

    return info


from common import create_io
from commands.base_server import BaseServer, Command


class GetImageInfoServer(BaseServer):
    name = 'GetImageInfoServer'
    guid = 'F89FA403EA244F489F0AC630BEE4CA56'
    command_list = [
        Command(
            name='получить информацию о картинке',
            uri='/execute',
            description='Команда получения информации о картинке. Например: Бот, получить информацию о картинке.',
            priority=9,
        ),
    ]

    # Путь к файлу сервера
    file_name = os.path.abspath(__file__)

    def _execute_body(self, rq: dict, **params: str) -> typing.Union[dict, str]:
        command = rq['command']
        command_name = rq['command_name']
        attachment = rq['attachment']

        if not attachment:
            raise Exception("Неправильная команда 'получить информацию о картинке': нужно передавать картинку.")

        img_file_io = create_io(attachment)

        info = get_image_info(img_file_io, pretty_json_str=True)
        return info


if __name__ == '__main__':
    server = GetImageInfoServer()
    server.run()
