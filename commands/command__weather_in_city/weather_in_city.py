#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Maia'


CODE_WEATHER_BY_DESCRIPTION = {
    '0': 'Торнадо',
    '1': 'Тропический шторм',
    '2': 'Ураган',
    '3': 'Сильные грозы',
    '4': 'Грозы',
    '5': 'Дождь со снегом',
    '6': 'Дождь с мокрым снегом',
    '7': 'Cнег и мокрый снег',
    '8': 'Изморозь',
    '9': 'Изморось',
    '10': 'Ледяной дождь',
    '11': 'Ливневые дожди',
    '12': 'Ливни',
    '13': 'Порывы снега',
    '14': 'Легкий снежный дождь',
    '15': 'Низовая метель',
    '16': 'Снег',
    '17': 'Град',
    '18': 'Мокрый снег',
    '19': 'Вихрь',
    '20': 'Туманно',
    '21': 'Легкий туман',
    '22': 'Дымка',
    '23': 'Бушующий ветер',
    '24': 'Ветренно',
    '25': 'Холодно',
    '26': 'Облачно',
    '27': 'В основном облачно (ночь)',
    '28': 'В основном облачно (день)',
    '29': 'Местами облачно (ночь)',
    '30': 'Местами облачно (день)',
    '31': 'Безоблачно (ночь)',
    '32': 'Солнечно',
    '33': 'Ясно (ночь)',
    '34': 'Ясно (день)',
    '35': 'Дождь с градом',
    '36': 'Жарко',
    '37': 'Изолированные грозы',
    '38': 'Рассеяные грозы',
    '39': 'Местами грозы',
    '40': 'Местами ливни',
    '41': 'Снегопад',
    '42': 'Местами снегпад',
    '43': 'Снегопад',
    '44': 'Местами облачно',
    '45': 'Грозовые ливни',
    '46': 'Снежные ливни',
    '47': 'Изолированные грозовые ливни',
    '3200': 'Недоступно'
}


def get_weather(city):
    """
    Функция возвращает описание погоды указанного населенный пункт.

    """

    url = "https://query.yahooapis.com/v1/public/yql?q=select item from weather.forecast where woeid in " \
          "(select woeid from geo.places(1) where text='{city}') and u='c'" \
          "&format=json&diagnostics=true".format(city=city)

    import requests
    rs = requests.get(url)

    query = rs.json().get('query')

    # Если query = None или query['results'] = None
    if not query or not query['results']:
        return "Не найден населенный пункт"

    item = query['results']['channel']['item']
    condition = item['condition']

    temp = condition['temp']
    code = condition['code']
    text = CODE_WEATHER_BY_DESCRIPTION[code]

    return 'Текущая погода в "{}": {} °C, {}'.format(city, temp, text)


if __name__ == '__main__':
    city = "Магнитогорск"
    print(get_weather(city))

    city = "[etcjcbyf"
    print(get_weather(city))

    city = ""
    print(get_weather(city))
