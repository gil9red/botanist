#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100
# TODO: логировать в файл
#

from config import LOGIN, PASSWORD


def get_logger(name):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')

    import sys
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


log = get_logger('mini_vk_bot')


# Отлов необработанныз исключений и закрытие
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    log.error(text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()
    log.debug("Бот запущен")

    command_prefix = 'Бот,'

    last_message_bot_id = None

    messages_get_values = {
        'out': 0,
        'count': 1,
        'time_offset': 60,
        'version': '5.67'
    }

    while True:
        try:
            rs = vk.method('messages.get', messages_get_values)
            # log.debug(rs)

            # Если ничего не пришло
            if not rs['items']:
                continue

            message_id = rs['items'][0]['id']
            from_user_id = rs['items'][0]['user_id']
            message = rs['items'][0]['body']

            # Бот реагирует только на сообщения, начинающиеся с префикса
            if not message.lower().startswith(command_prefix.lower()):
                continue

            log.debug('From user #%s, message (#%s): "%s"', from_user_id, message_id, message)
            command = message[len(command_prefix):].strip()

            # TODO: для каждой команды отдельный поток создавать
            # Пример: https://www.ibm.com/developerworks/ru/library/l-python_part_9/index.html#N10078
            # только поток нужно без демона использовать, демон указывает что при закрытии главного потока
            # должны и потоки-демоны завершиться, что для текущей задачи не будет правильным
            
            # Выполнение команды
            import commands
            message = commands.execute(command)

            # Если ответа от бота нет
            if not message:
                message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

            log.debug(message)

            last_message_bot_id = vk.method('messages.send', {'user_id': from_user_id, 'message': message})
            messages_get_values['last_message_id'] = last_message_bot_id

        except Exception as e:
            log.exception('Error:')

        finally:
            import time
            time.sleep(3)
