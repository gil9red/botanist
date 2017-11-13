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

    # Бот реагирует только на сообщения, начинающиеся с префикса
    if not message.lower().startswith(command_prefix.lower()):
        return

    # Если сообщение пришло из групповой беседы, в chat_id будет число, иначе None
    chat_id = item.get('chat_id')
    if chat_id:
        log.debug('From chat #%s from user #%s, message (#%s): "%s"',
                  chat_id, from_user_id, message_id, message)
    else:
        log.debug('From user #%s, message (#%s): "%s"', from_user_id, message_id, message)

    command = message[len(command_prefix):].strip()

    attachment = None
    attachment_type = None

    # Выполнение команды
    try:
        rs = commands.execute(command)

        # Если нет результата, берем значение из поля error. В штатной ситуации
        # result может быть null, error тоже null, а attachment содержать значения
        message = rs['result']
        if not message:
            message = rs['error']

        attachment = rs['attachment']
        attachment_type = rs['attachment_type']

    except Exception as e:
        log.exception("Error:")

        import traceback
        message = 'При выполнении команды "{}" произошла ошибка: ' \
                  '"{}":\n\n{}'.format(command, e, traceback.format_exc())

    # Если ответа от бота нет
    if not message and not attachment:
        message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

    log.debug('Message: "%s"', message)

    # Подготавливаем словарь с параметрами запроса
    messages_send_values = {
        'forward_messages': message_id,
    }

    # Если сообщение пришло из групповой беседы
    if chat_id:
        messages_send_values['chat_id'] = chat_id
    else:
        messages_send_values['user_id'] = from_user_id

    # Если пришел прикрепленный файл/файлы
    if attachment:
        attachment = common.get_vk_attachment(vk, attachment, attachment_type)
        messages_send_values['attachment'] = attachment

    # Сообщение может быть само по себе или вместе с attachment
    if message:
        messages_send_values['message'] = message

    print('messages_send_values:', messages_send_values)

    last_message_bot_id = vk.method('messages.send', messages_send_values)
    messages_get_values['last_message_id'] = last_message_bot_id


if __name__ == '__main__':
    # Просмотр статистики приложения: https://vk.com/stats?act=api&aid=5356487
    # Специально использую свое приложение (app_id=5356487) для работы с API, т.к. был случай блокировки
    # аккаунта из-за сбоя спам-системы, хотя за ограничения запросов в секунду не выходил:
    #    Здравствуйте, Илья!
    #    Мы разобрались в ситуации: к сожалению, наша антиспам-система несколько погорячилась сегодня при блокировке
    #    Вашей страницы. Сейчас страница разблокирована.
    #
    #    В будущем мы рекомендуем использовать собственное приложение при работе с API, о его создании написано в
    #    документации: https://vk.cc/7ehNod. Чтобы подобных недоразумений не возникало, при составлении запросов к
    #    API следует использовать API_ID своего приложения.
    #
    #    С уважением,
    #    Команда Поддержки ВК
    #
    #    16 окт 2017 в 14:54
    # TODO: vk -> vk_session, vk = vk_session.get_api()
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD, app_id=5356487)
    vk.auth()
    log.debug("Бот запущен")

    messages_get_values = {
        'count': 1,
        'time_offset': 60,
    }

    while True:
        try:
            messages_get(vk)

        except Exception as e:
            log.exception('Error:')

        finally:
            time.sleep(1)

    # TODO: переписать работу бота на longpoll: https://github.com/python273/vk_api/tree/master/examples/messages_bot
    # Мини-пример:
    # # TODO: при тестировании от своего же диалога, нужно быть осторожным, т.к. тут аналога поля last_message_id
    # #       нет, поэтому бот будет отвечать сразу же самому себе, так что нужно предусмотреть механизм ответа
    # #       и не отвечать на сообщения, на которое ответ уже был отправлен
    # import vk_api
    # from vk_api.longpoll import VkLongPoll, VkEventType
    #
    # vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    # vk_session.auth()
    #
    # vk = vk_session.get_api()
    # longpoll = VkLongPoll(vk_session)
    #
    # for event in longpoll.listen():
    #     if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    #         print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
    #
    #         vk.messages.send(
    #             user_id=event.user_id,
    #             message=event.text.upper()
    #         )
    #         print('ok')
