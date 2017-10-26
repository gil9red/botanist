#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: упростить код, использующий typing
#       https://docs.python.org/3/library/typing.html
#       https://www.python.org/dev/peps/pep-0484/
#       https://www.python.org/dev/peps/pep-0526/

from typing import Union, List, Dict
from collections import namedtuple

FileAttachment = namedtuple('FileAttachment', ['extension', 'content'])


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        import sys
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def make_backslashreplace_console():
    # При выводе юникодных символов в консоль винды
    # Возможно, не только для винды, но и для любой платформы стоит использовать
    # эту настройку -- мало какие проблемы могут встретиться
    import sys
    if sys.platform == 'win32':
        import codecs

        try:
            sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
            sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')

        except AttributeError:
            # ignore "AttributeError: '_io.BufferedWriter' object has no attribute 'encoding'"
            pass


import enum


class StrEnum(str, enum.Enum):
    pass


@enum.unique
class AttachmentType(StrEnum):
    IMAGE = 'image'
    GIF = 'gif'
    LIST_IMAGE = 'list_image'


def create_attachment(attachment: Union[FileAttachment, List[FileAttachment]], attachment_type: Union[AttachmentType, str, None]) -> Union[Dict[str, str], List[Dict[str, str]], None]:
    if attachment is None or attachment_type is None:
        return

    import base64

    if isinstance(attachment_type, str):
        attachment_type = AttachmentType(attachment_type)

    if attachment_type == AttachmentType.LIST_IMAGE:
        items = []

        for file_attachment in attachment:
            content = file_attachment.content
            content = base64.b64encode(content).decode('utf-8')

            items.append({
                'extension': file_attachment.extension,
                'content': content,
            })

        return items

    elif attachment_type in [AttachmentType.IMAGE, AttachmentType.GIF]:
        content = attachment.content
        content = base64.b64encode(content).decode('utf-8')

        return {
            'extension': attachment.extension,
            'content': content,
        }

    raise Exception('Unknown attachment_type="{}"'.format(attachment_type))


def upload_images(vk, file_names) -> str:
    import vk_api
    upload = vk_api.VkUpload(vk)
    rs = upload.photo_messages(file_names)

    # Составление названия изображений: https://vk.com/dev/messages.send
    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in rs)
    return attachment


def upload_doc(vk, file_name) -> str:
    import vk_api
    upload = vk_api.VkUpload(vk)
    rs = upload.document(file_name)

    # Составление названия документа: https://vk.com/dev/messages.send
    attachment = 'doc{owner_id}_{id}'.format(**rs[0])
    return attachment


def get_vk_attachment(vk, attachment: Union[Dict[str, str], List[Dict[str, str]]], attachment_type: Union[AttachmentType, str, None]) -> Union[str, None]:
    if attachment is None or attachment_type is None:
        return

    import base64
    import io

    if isinstance(attachment_type, str):
        attachment_type = AttachmentType(attachment_type)

    # Список картинок
    if attachment_type == AttachmentType.LIST_IMAGE:
        items = []

        for item in attachment:
            content = item['content']

            img = base64.b64decode(content.encode('utf-8'))
            img_file = io.BytesIO(img)
            items.append(img_file)

        attachment = upload_images(vk, items)
        return attachment

    # Картинка или гифка
    elif attachment_type in [AttachmentType.IMAGE, AttachmentType.GIF]:
        content = attachment['content']

        img = base64.b64decode(content.encode('utf-8'))
        img_file = io.BytesIO(img)

        if attachment_type == AttachmentType.IMAGE:
            attachment = upload_images(vk, img_file)

        else:
            # Нужно подсказать методу vk_api о типе документа
            img_file.name = 'file.' + attachment['extension']
            attachment = upload_doc(vk, img_file)

        return attachment

    else:
        raise Exception('Unknown attachment_type="{}"'.format(attachment_type))
