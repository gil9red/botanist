#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100


from common import get_logger, make_backslashreplace_console
make_backslashreplace_console()

from config import LOGIN, PASSWORD

log = get_logger('mini_vk_bot', file='bot.log')


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

    messages_get_values = {
        'count': 1,
        'time_offset': 60,
        'version': '5.68'
    }

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
        message = commands.execute(command)

    except Exception as e:
        log.exception("Error:")

        import traceback
        message = 'При выполнении команды "{}" произошла ошибка: ' \
                  '"{}":\n\n{}'.format(command, e, traceback.format_exc())

    # Если ответа от бота нет
    if not message:
        message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

    log.debug('Message: "%s"', message)

    messages_send_values = {
        'message': message,
        'version': '5.67',
        'forward_messages': message_id,
    }

    # Если сообщение пришло из групповой беседы
    if chat_id:
        messages_send_values['chat_id'] = chat_id
    else:
        messages_send_values['user_id'] = from_user_id

    print('messages_send_values:', messages_send_values)
    # quit()
    last_message_bot_id = vk.method('messages.send', messages_send_values)
    messages_get_values['last_message_id'] = last_message_bot_id


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()
    log.debug("Бот запущен")

    while True:
        try:
            messages_get(vk)

        except Exception as e:
            log.exception('Error:')

        finally:
            time.sleep(1)
