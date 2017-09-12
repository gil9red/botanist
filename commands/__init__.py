#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: каждая команда отдельный http вебсервер, к которым бот шлет запросы в формате json
# TODO: добавить команду курс валют
# TODO: добавить команду курс криптовалют
# TODO: поддержать опциональную команду график к командам курса валют, которая вернет картинку с графиком курса
#       диапазон курса выбрать опытным путем
# TODO: добавить команду поиска на торрентах, которая вернет ссылку на .torrent файл
# TODO: добавить команду для возврата гифки из https://giphy.com/ (https://developers.giphy.com/)
#       аналог такого делает бот битрикса. Команды поиска похоже нужно будет переводить на английский
# TODO: команда превращения ссылки в короткую (пусть будет выбор через какой сервис сокращать ссылку)
# TODO: команду hex2str и str2hex
# TODO: команду gin2str и str2bin
# TODO: команду генерации qrcode, который или ссылкой возвращается или как картинка
# TODO: команду возврата поздравления к др/юбилею для папы/мамы/бабушки и т.п.
# TODO: команды генерации в base64 и раскодирования из base64
# TODO: команду добавления напоминаний, типа "Бот, напомни о встрече у Ленина в 12:30"
# TODO: команду угадывания что на картинке
# TODO: команду ретуши фотографии -- например faceapp умеет добавлять улыбку и т.п.

ALL_COMMANDS = {
    'насмеши': 'Случайная цитата башорга',
    'ругнись': 'Напиши кого бот отругает. Например: "Бот, ругнись петр иваныч"',
    'погода': 'Погода в указанном населенном пункте. Например: "Бот, погода магнитогорск" или '
              '"бот, погода село кукуево"',
    # 'что посмотреть': 'Рандомная ссылка на кинопоиск',
    # 'котики': ':3',
    'команды': 'Показать список команд',
    'курс валют': 'Показать текущий курс евро и доллара'
}


def execute(command):
    # TODO: кроме результата команды лучше писать что за команда
    # Пример: Бот: результат выполнения команды: "погода магнитогорск"
    #         23 C, облачно
    #
    # Любой ответ от бота нужно начинать с "Бот: "
    
    # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки
    if not any(command.lower().startswith(x) for x in ALL_COMMANDS):
        return 'Получена неизвестная команда "{}".\n' \
               'Чтобы узнать команды введи: "Бот, команды"'.format(command)

    else:
        message = ''

        # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
        execute_command = command.lower()

        if execute_command.startswith('команды'):
            return '\n'.join('{}: {}'.format(k, v) for k, v in ALL_COMMANDS.items())

        elif execute_command.startswith('насмеши'):
            from commands import fun
            return fun.get_random_quote()

        elif execute_command.startswith('ругнись'):
            # Вытаскивание имени того, кого нужно обругать
            name = command[len('ругнись'):].strip()
            if not name:
                name = 'Бот'

            from commands import damn
            return damn.damn(name)

        elif execute_command.startswith('курс валют'):
            from commands import currency
            rate_list = currency.exchange_rate(['EUR', 'USD'])
            text = ', '.join(rate_list)
            return text

        elif execute_command.startswith('погода'):
            city = command[len('погода'):].strip()
            if not city:
                return "Неправильная команда 'погода': не указан населенный пункт"

            from commands import weather_in_city
            return weather_in_city.get_weather(city)

    return message
