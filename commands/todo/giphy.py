#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://developers.giphy.com/docs/#search-endpoint
# https://developers.giphy.com/explorer/

URL_SEARCH = 'https://api.giphy.com/v1/gifs/search?api_key={}&limit=1&offset={}&rating=G&lang=ru&q={}'
API_KEY = '80efb56295eb4277bc18d52771529a10'


# import requests
# rs = requests.get('https://media1.giphy.com/media/PhudO5SeUmbQI/giphy.gif')
# open('file_name.gif', 'wb').write(rs.content)
#
# quit()

def get_gif(text):
    import random
    offset = random.randrange(0, 100)

    url = URL_SEARCH.format(API_KEY, offset, text)

    import requests
    rs = requests.get(url)
    print(rs)
    return rs.json()


if __name__ == '__main__':
    print(get_gif('Котята'))
    print(get_gif('Cats'))
    print(get_gif('   '))
    print(get_gif('dfsdfsdf'))
