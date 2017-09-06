#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, jsonify, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

from commands import generate_response, DEBUG


# @app.route("/")
# def index():
#     return jsonify({
#         'name': 'damn'
#     })


@app.route("/execute", methods=['POST'])
def execute():
    request_text = request.data.decode('utf-8')
    print('request_text:', request_text)

    import json
    rq = json.loads(request_text)
    print('rq:', rq)

    if 'command' not in rq:
        raise Exception("Not found key 'command'.")

    command = rq['command']

    if DEBUG:
        result = command.upper()
    else:
        from commands.command__weather_in_city.weather_in_city import get_weather
        result = get_weather(command)

    ok = result is not None

    rs = generate_response(result, ok)
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
        port=55003,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
