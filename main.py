#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100


import common
common.make_backslashreplace_console()

from config import LOGIN, PASSWORD

log = common.get_logger('mini_vk_bot', file='bot.log')


# Отлов необработанныз исключений и закрытие
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    log.error(text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


import commands
import time


def messages_get(vk):
    command_prefix = 'Бот,'

    rs = vk.method('messages.get', messages_get_values)
    # log.debug(rs)

    # Если ничего не пришло
    if not rs['items']:
        return

    item = rs['items'][0]
    message_id = item['id']
    from_user_id = item['user_id']
    message = item['body']

    # Если сообщение пришло из групповой беседы, в chat_id будет число, иначе None
    chat_id = item.get('chat_id')

    # Бот реагирует только на сообщения, начинающиеся с префикса
    if not message.lower().startswith(command_prefix.lower()):
        return

    if chat_id:
        log.debug('From chat #%s from user #%s, message (#%s): "%s"',
                  chat_id, from_user_id, message_id, message)
    else:
        log.debug('From user #%s, message (#%s): "%s"', from_user_id, message_id, message)

    command = message[len(command_prefix):].strip()

    # Выполнение команды
    try:
        rs = commands.execute(command)

        # Сначала предполагаем что могла вернуться ошибка, если нет, тогда
        # смотрим в результат
        message = rs['error']
        if not message:
            message = rs['result']

        attachment = rs['attachment']
        data_type = rs['type']

    except Exception as e:
        log.exception("Error:")

        import traceback
        message = 'При выполнении команды "{}" произошла ошибка: ' \
                  '"{}":\n\n{}'.format(command, e, traceback.format_exc())
        data_type = common.TYPE_TEXT
        attachment = None

    # Если ответа от бота нет
    if not message and not attachment:
        message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

    log.debug('Message: "%s"', message)

    # Подготавливаем словарь с параметрами запроса
    messages_send_values = {
        'version': '5.67',
        'forward_messages': message_id,
    }

    # Если сообщение пришло из групповой беседы
    if chat_id:
        messages_send_values['chat_id'] = chat_id
    else:
        messages_send_values['user_id'] = from_user_id

    # Если пришел прикрепленный файл/файлы
    if attachment:
        attachment = common.get_vk_attachment(vk, attachment, data_type)
        messages_send_values['attachment'] = attachment

    # Сообщение может быть само по себе или вместе с attachment
    if message:
        messages_send_values['message'] = message

    print('messages_send_values:', messages_send_values)

    last_message_bot_id = vk.method('messages.send', messages_send_values)
    messages_get_values['last_message_id'] = last_message_bot_id


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()
    log.debug("Бот запущен")

    messages_get_values = {
        'count': 1,
        'time_offset': 60,
        'version': '5.68'
    }

    while True:
        try:
            messages_get(vk)

        except Exception as e:
            log.exception('Error:')

        finally:
            time.sleep(1)
