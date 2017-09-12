#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, jsonify, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

from commands import (
    generate_response,
    generate_request,
    get_request_data,
    ALL_COMMAND_BY_URL,
    ALL_COMMAND_NAME_BY_DESCRIPTION
)

# @app.route("/")
# def index():
#     return jsonify({
#         'name': 'damn'
#     })


@app.route("/get_commands", methods=['GET', 'POST'])
def get_commands(as_result=None):
    print(request.args)
    if as_result or 'as_result' in request.args:
        result = '\n'.join('{}: {}'.format(k, v) for k, v in sorted(ALL_COMMAND_NAME_BY_DESCRIPTION.items(), key=lambda x: x[0]))

        rs = generate_response(result, ok=True)
        return jsonify(rs)

    return jsonify(ALL_COMMAND_NAME_BY_DESCRIPTION)


@app.route("/execute", methods=['POST'])
def execute():
    rq = get_request_data(request)
    command = rq['command']

    # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
    execute_command = command.lower()

    # TODO: при обработке команды учитывать в ней опечатки, использовать алгоритм
    # Damerau–Levenshtein distance (Расстояние Дамерау — Левенштейна) для определения опечатки
    # и наиболее похожей команде (для вычисления расстояний между строками)
    # https://github.com/gil9red/SimplePyScripts/blob/12c303ea76c1f2c2983e38c96f3acf4c5ecd4e50/Damerau%E2%80%93Levenshtein_distance__misprints__%D0%BE%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%BA%D0%B8/use__pyxdameraulevenshtein/find_command.py
    #
    # execute_command = find_command(execute_command)

    # Обработка собственной команды
    if execute_command == 'команды':
        # return redirect('/get_commands?as_result')
        return get_commands(as_result=True)

    error = None

    # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки
    if not any(execute_command.startswith(x) for x in ALL_COMMAND_BY_URL):
        result = 'Получена неизвестная команда "{}".\n' \
                 'Чтобы узнать команды введи: "Бот, команды"'.format(command)
        ok = True

    else:
        result = None
        ok = False

        for command_name, url in ALL_COMMAND_BY_URL.items():
            if execute_command.startswith(command_name.lower()):
                command_module = command[len(command_name):].strip()
                print(command_module, url)

                import requests
                rs = requests.post(url, json=generate_request(command_module))
                rs = rs.json()
                print(rs)

                result = rs['result']
                ok = True

                break

        if result is None:
            error = 'Что-то пошло не так: команда "{}" не была распознана'.format(command)

    rs = generate_response(result, ok, error)
    print('  rs:', rs)

    return jsonify(rs)


@app.errorhandler(Exception)
def all_exception_handler(error):
    import traceback
    print('Error', error, traceback.format_exc())

    rs = generate_response(result=None, ok=False, error=str(error))
    print('  rs:', rs)

    return jsonify(rs)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(
        port=55000,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
