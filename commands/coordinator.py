#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, jsonify, request, redirect
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

from commands import generate_response, ALL_COMMAND_MODULE, ALL_COMMAND_BY_URL, ALL_COMMAND_NAME_BY_DESCRIPTION

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
    # TODO: нужно определить в какой модуль перенаправить запрос

    request_text = request.data.decode('utf-8')
    print('request_text:', request_text)

    import json
    rq = json.loads(request_text)
    print('rq:', rq)

    if 'command' not in rq:
        raise Exception("Not found key 'command'.")

    command = rq['command']

    # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
    execute_command = command.lower()

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
                rs = requests.post(url, json={'command': command_module})
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

    # :param threaded: should the process handle each request in a separate
    #                  thread?
    # :param processes: if greater than 1 then handle each request in a new process
    #                   up to this maximum number of concurrent processes.
    app.threaded = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=55000)

    # # Public IP
    # app.run(host='0.0.0.0')
