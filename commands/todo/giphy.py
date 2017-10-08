#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# # TODO: пофиксить костыль
# if message.endswith('.gif'):
#     time.sleep(0.3)
#     # rs = vk.method('photos.getWallUploadServer')
#     # rs = vk.method('docs.getUploadServer')
#     rs = vk.method('photos.getMessagesUploadServer')
#     upload_url = rs['upload_url']
#
#     log.debug('Загрузка картинки на сервер: "%s"', upload_url)
#     import requests
#     rs = requests.post(upload_url, files={'photo': open(r'C:\Users\ipetrash\PycharmProjects\mini_vk_bot\commands\file_name.gif', 'rb')})
#     # rs = requests.post(upload_url, files={'file': open(r'C:\Users\ipetrash\PycharmProjects\mini_vk_bot\commands\file_name.gif', 'rb')})
#     rs = rs.json()
#     log.debug('Response: "%s"', repr(rs))
#
#     time.sleep(0.3)
#     log.debug('Сохранение загруженной картинки на сервер вк')
#     # rs = vk.method('photos.saveWallPhoto', {'photo': rs['photo'], 'server': rs['server'], 'hash': rs['hash']})
#     rs = vk.method('photos.saveMessagesPhoto', {'photo': rs['photo'], 'server': rs['server'], 'hash': rs['hash']})
#     # rs = vk.method('docs.save', {'file': rs['file']})
#     log.debug('Response: "%s"', repr(rs))
#
#     OWNER_ID = BOT_USER_ID
# TODO: OWNER_ID from rs
#     attachments = 'photo{}_{}'.format(OWNER_ID, rs[0]['id'])
#     # attachments = 'doc{}_{}'.format(OWNER_ID, rs[0]['id'])
#     log.debug('Поле attachments для загруженной картинки: %s.', attachments)
#
#     # attachments = 'https://psv4.userapi.com/c816331/u52658091/docs/f240396aa2e5/file_name.gif?extra=xxet7trqGKGXNds9H9dnRioQYyiAi8-dfCJXetNElKhAR15P1u4wscSiF74HlkOHCddNHdVx7G4bVUY_nZU6zRTd-5nwGTHz8mYNXMv9aXggrPZnTvaPtg'
#     # attachments = 'https://im0-tub-ru.yandex.net/i?id=9f2fb4e8d6e6e303dbb5d1af69593ce9-l&n=13'
#
#     # messages_send_values['attachments'] = message
#     messages_send_values['attachments'] = attachments



# https://developers.giphy.com/docs/#search-endpoint
# https://developers.giphy.com/explorer/

URL_SEARCH = 'https://api.giphy.com/v1/gifs/search?api_key={}&limit=1&offset={}&rating=G&lang=ru&q={}'
API_KEY = '80efb56295eb4277bc18d52771529a10'


import requests
rs = requests.get('https://media1.giphy.com/media/PhudO5SeUmbQI/giphy.gif')
open('file_name.gif', 'wb').write(rs.content)

quit()

def get_gif(text):
    import random
    offset = random.randrange(0, 100)

    url = URL_SEARCH.format(API_KEY, offset, text)

    import requests
    rs = requests.get(url)
    print(rs)
    print(rs.json())

    # # Перемешиваем список цитат и берем последний элемент
    # import random
    # random.shuffle(CACHE_QUOTES)
    #
    # # Удаление и возврат последнего элемента из списка
    # return CACHE_QUOTES.pop()


if __name__ == '__main__':
    print(get_gif('Котята'))
    print(get_gif('Cats'))
    print(get_gif('   '))
