#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://developers.giphy.com/docs/#search-endpoint
# https://developers.giphy.com/explorer/

API_KEY = '80efb56295eb4277bc18d52771529a10'
URL_SEARCH = 'https://api.giphy.com/v1/gifs/search?api_key={}&q={}&limit=25&offset=0&rating=G&lang=ru'


def get_gif(text: str) -> str:
    url = URL_SEARCH.format(API_KEY, text)

    import requests
    rs = requests.get(url)
    json_data = rs.json()
    # print(rs, json_data)

    result = json_data['data']
    if not result:
        return ''

    import random
    data = random.choice(result)

    return data['images']['original']['url']


if __name__ == '__main__':
    def check_rs_url(url):
        if not url:
            print('not found')
        else:
            print(url)

            dir_name = 'gif'

            import os
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

            # https://media0.giphy.com/media/LypkRynk8We7C/giphy-downsized.gif -> LypkRynk8We7C__giphy-downsized.gif
            parts = url.split('/')
            file_name = dir_name + '/' + parts[-2] + '__' + parts[-1]

            with open(file_name, mode='wb') as f:
                import requests
                rs = requests.get(url)

                f.write(rs.content)


    url = get_gif('Котята')
    check_rs_url(url)

    url = get_gif('Cats')
    check_rs_url(url)

    url = get_gif('   ')
    check_rs_url(url)

    url = get_gif('dfsdfsdf')
    check_rs_url(url)
