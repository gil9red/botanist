#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: брать таблицу серверов из ajax и показывать из базы информацию о них.
#       круто будет выглядеть когда на странице можно увидеть какие из серверов запущены,
#       а какие нет.

import sys


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)


from commands import execute
import db

import cherrypy
from jinja2 import Template


class Root:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def execute(self):
        rq = cherrypy.request.json
        print(rq)

        command = rq['command']

        try:
            rs = execute(command)

        except Exception as e:
            import traceback

            from collections import OrderedDict
            result = OrderedDict()
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()

            return result

        return rs

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_all_server_with_commands(self):
        return db.get_all_server_with_commands()

    @cherrypy.expose
    def index(self):
        text = """
<html>
    <head>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
        <style>
            /* 
                https://stackoverflow.com/a/7220510/5909792
                FOR function syntaxHighlight
            */
            pre {outline: 1px solid #ccc; padding: 5px; margin: 5px; white-space:pre-wrap; }
            .string { color: green; }
            .number { color: darkorange; }
            .boolean { color: blue; }
            .null { color: magenta; }
            .key { color: red; }
            
            table {
                border-collapse: collapse; /* Убираем двойные линии между ячейками */
            }
                /* Увеличим заголовок таблиц */
                table > caption {
                    font-size: 150%;
                }
    
                th {
                    font-size: 120%;
                }
                td, th {
                    border: 1px double #333; /* Рамка таблицы */
                    padding: 5px;
                }
                
                table th {
                    border-width: 1px;
                    padding: 8px;
                    border-style: solid;
                    border-color: #666666;
                    background-color: #c0c0c0;
                    text-align: left;
                }
                
                table.inner {
                    font-size: 90%;
                    width: 100%;
                    
                    border-collapse: collapse;
                }
                    table.inner td, table.inner th {
                        border-bottom: 1px double rgba(0, 0, 0, 0);
                        border-top: 1px double rgba(0, 0, 0, 0);
                    }
                    table.inner td:first-child, table.inner th:first-child {
                        border-left: 1px double rgba(0, 0, 0, 0);
                    }
                    table.inner th:last-child, table.inner td:last-child {
                        border-right: 1px double rgba(0, 0, 0, 0);
                    }
                    table.inner tr td {
                        border-bottom: 1px double rgba(0, 0, 0, 1);
                    }
                    table.inner tr:last-child td {
                        border-bottom: 1px double rgba(0, 0, 0, 0);
                    }
                    
                    table.inner th {
                        border-bottom: 1px double rgba(0, 0, 0, 1);
                    }
                    
                    table.inner th {
                        background-color: #dedede;
                    }
                
                table tr[availability="1"] td, table tr[availability="1"] th {
                    /* TODO: разобраться почему два раза выделяет td */
                    background-color: rgba(34, 177, 76, 0.35);
                }
                
        </style>
    </head>

    <body>
        <script type='text/javascript'>
            // https://stackoverflow.com/a/7220510/5909792
            function syntaxHighlight(json) {
                json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                    var cls = 'number';
                    if (/^"/.test(match)) {
                        if (/:$/.test(match)) {
                            cls = 'key';
                        } else {
                            cls = 'string';
                        }
                    } else if (/true|false/.test(match)) {
                        cls = 'boolean';
                    } else if (/null/.test(match)) {
                        cls = 'null';
                    }
                    return '<span class="' + cls + '">' + match + '</span>';
                });
            }
            
            function create_img_base64(attachment) {
                return '<img src="data:image/' + attachment.extension + ';base64, ' + attachment.content + '">';
            }

            function fill_raw_result() {
                var json_data = window.rs_json;

                if (!$('#show_attachment_value > input').is(':checked') && window.attachment != null) {
                    var attachment_length = JSON.stringify(window.attachment).length;
                    var attachment_text = '<скрыто ' + attachment_length + ' символов>';

                    // Clone
                    json_data = JSON.parse(JSON.stringify(json_data));
                    json_data.attachment = attachment_text;
                }

                var json_str = JSON.stringify(json_data, undefined, 4);
                console.log(json_str);

                json_str = syntaxHighlight(json_str);

                $('.raw_result.show > pre').html(json_str);
                $('.raw_result.show').show();
            }

            function execute() {
                $('.raw_result.show').hide();
                $('.result.show').hide();

                window.rs_json = null;
                window.attachment = null;

                $.ajax({
                    type: 'POST',
                    url: "/execute",
                    contentType: "application/json",
                    dataType: "json",  // тип данных загружаемых с сервера
                    processData: false,
                    data: JSON.stringify({'command': $('#update_box').val()}),

                    success: function(data) {
                        window.rs_json = data;
                        window.attachment = data.attachment;

                        if (window.attachment != null) {
                            $('#show_attachment_value').show();
                        } else {
                            $('#show_attachment_value').hide();
                        }

                        fill_raw_result();

                        var result_body = "<div>";
                        result_body += '<pre>' + data.result + '</pre>';

                        switch (data.type) {
                            case 'image':
                            case 'gif':
                                result_body += '<br>';
                                result_body += create_img_base64(data.attachment);

                                break;

                            case 'list_image':
                                result_body += '<br>';

                                data.attachment.forEach(function(item, i, arr) {
                                    result_body += create_img_base64(item) + "<br><br>";
                                });

                                break;
                        }

                        result_body += '</div>';

                        console.log(result_body);

                        $('.result.show > .body').html(result_body);
                        $('.result.show').show();
                    },

                    error: function (jqXHR, exception) {
                        var msg = '';

                        if (jqXHR.status === 0) {
                            msg = 'Not connect. Verify Network.';
                        } else if (jqXHR.status == 404) {
                            msg = 'Requested page not found. [404]';
                        } else if (jqXHR.status == 500) {
                            msg = 'Internal Server Error [500].';
                        } else if (exception === 'parsererror') {
                            msg = 'Requested JSON parse failed.';
                        } else if (exception === 'timeout') {
                            msg = 'Time out error.';
                        } else if (exception === 'abort') {
                            msg = 'Ajax request aborted.';
                        } else {
                            msg = 'Uncaught Error. ' + jqXHR.responseText;
                        }

                        console.log(msg);
                        $('.raw_result.show > pre').html(msg);
                        $('.raw_result.show').show();
                    },
                });
            }
            
            function load_servers_info() {
                $.ajax({
                    url: '/get_all_server_with_commands',
                    dataType: "json",  // тип данных загружаемых с сервера
                    success: function(data) {
                        console.log(data);
                        console.log(JSON.stringify(data));
        
                    },
        
                    error: function(data) {
                        var msg = '';
                        
                        if (jqXHR.status === 0) {
                            msg = 'Not connect. Verify Network.';
                        } else if (jqXHR.status == 404) {
                            msg = 'Requested page not found. [404]';
                        } else if (jqXHR.status == 500) {
                            msg = 'Internal Server Error [500].';
                        } else if (exception === 'parsererror') {
                            msg = 'Requested JSON parse failed.';
                        } else if (exception === 'timeout') {
                            msg = 'Time out error.';
                        } else if (exception === 'abort') {
                            msg = 'Ajax request aborted.';
                        } else {
                            msg = 'Uncaught Error. ' + jqXHR.responseText;
                        }
                        
                        console.log(msg);
                        alert(msg);
                    }
                });
            }
            
            $(document).ready(function() {
                load_servers_info();
            });
            
        </script>
        
        
        <table>
            <tr>
                {% for header in server_headers %}
                    <th>{{ header }}</th>
                {% endfor %}
            </tr>
        
            {% for server in all_server_with_commands %}
                <tr availability="{{ server["availability"] }}">
                    <td>{{ server["name"] }}</td>
                    <td>{{ server["guid"] }}</td>
                    <td>{{ server["url"] }}</td>
                    <td>{{ server["availability"] }}</td>
                    <td>{{ server["datetime_last_availability"] }}</td>
                    <td>{{ server["datetime_last_request"] }}</td>
                    <td>{{ server["file_name"] }}</td>
                </tr>
                
                <tr availability="{{ server["availability"] }}">
                    <td></td>
                    <td style="padding: 0px" colspan="99">
                        <table class="inner">
                            <tr>
                                <th style="width: 15%;">{{ command_headers[0] }}</th>
                                <th style="width: 35%;">{{ command_headers[1] }}</th>
                                <th>{{ command_headers[2] }}</th>
                            </tr>
                            
                            {% for command in server["command_list"] %}
                                <tr>
                                    <td>{{ command[0] }}</td>
                                    <td>{{ command[1] }}</td>
                                    <td>{{ command[2] }}</td>
                                </tr>
                            {% endfor %}
                        </table>
                    </td>
                </tr>
                
                {% if loop.index < all_server_with_commands|length %}
                <tr><td colspan="99"></td></tr>
                {% endif %}
            {% endfor %}
        </table>
        
        <br>
        <p>Input command:</>
        <br>
        <input type='text' id='update_box' value='str2hex Привет Мир!' onkeydown="if (event.keyCode == 13) { execute(); return false; }" size='100' />
        <input type='submit' value='execute' onClick='execute(); return false' />
        
        <br>
        
        <div class="result show" style="display: none; width: 50%;">
            <p>Result:</p>
            <div class="body"></div>
        </div>
        
        <br>
        <div class="raw_result show" style="display: none; width: 50%;">
            <p>Raw result:</p>
            <div style="display: none" id="show_attachment_value"><input type="checkbox" onClick='fill_raw_result()'>Show attachment value</div>
            <pre></pre>
        </div>
                
    </body>
</html>
"""
        template = Template(text)
        return template.render(
            table_command=db.get_all_command_name_by_description().items(),

            server_headers=['Название', 'GUID', 'Url', 'Доступность', 'Время последней доступности',
                            'Дата последнего запроса к серверу', 'Полный путь к файлу сервера'],
            command_headers=['Команда', 'Описание', 'Url'],
            all_server_with_commands=db.get_all_server_with_commands(),
        )


if __name__ == '__main__':
    # Set port
    cherrypy.config.update({'server.socket_port': 9090})

    # Autoreload off
    cherrypy.config.update({'engine.autoreload.on': False})

    cherrypy.quickstart(Root())
