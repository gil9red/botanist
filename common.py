#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Union, List, Dict
from collections import namedtuple

FileAttachment = namedtuple('FileAttachment', ['content', 'extension'])


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


AnyAttachmentType = Union[AttachmentType, str, None]
AnyAttachment = Union[FileAttachment, List[FileAttachment]]
AttachmentRs = Union[Dict[str, str], List[Dict[str, str]], None]


def generate_request(command_name: str = '', command: str = '', attachment: AnyAttachment = None) -> dict:
    return {
        'command_name': command_name,
        'command': command,
        'attachment': attachment,
    }


def create_attachment(attachment: AnyAttachment, attachment_type: AnyAttachmentType) -> AttachmentRs:
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


def create_io(attachment):
    import base64
    import io

    content = attachment['content']

    img = base64.b64decode(content.encode('utf-8'))
    img_file = io.BytesIO(img)
    img_file.name = 'file.' + attachment['extension']

    return img_file


def get_vk_attachment(vk, attachment: AttachmentRs, attachment_type: AnyAttachmentType) -> Union[str, None]:
    if attachment is None or attachment_type is None:
        return

    if isinstance(attachment_type, str):
        attachment_type = AttachmentType(attachment_type)

    # Список картинок
    if attachment_type == AttachmentType.LIST_IMAGE:
        items = [create_io(item) for item in attachment]

        attachment = upload_images(vk, items)
        return attachment

    # Картинка или гифка
    elif attachment_type in [AttachmentType.IMAGE, AttachmentType.GIF]:
        file_io = create_io(attachment)

        if attachment_type == AttachmentType.IMAGE:
            attachment = upload_images(vk, file_io)
        else:
            attachment = upload_doc(vk, file_io)

        return attachment

    else:
        raise Exception('Unknown attachment_type="{}"'.format(attachment_type))
