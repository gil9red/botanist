#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: добавить таблицу серверов и показывать из базы информацию о них.
#       круто будет выглядеть когда на странице можно увидеть какие из серверов запущены,
#       а какие нет.
# TODO: показывать какие команды к каким серверам относятся


import sys


# Добавление пути к папке с проектом, чтобы заработал импорт пакета commands и таких модулей
# как db.py и common.py
import pathlib
current_dir = pathlib.Path(__file__).parent.resolve()
dir_up = str(current_dir.parent.resolve())

if dir_up not in sys.path:
    sys.path.append(dir_up)


from commands import execute

import cherrypy


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
    def index(self):
        # TODO: добавить модуль генерации по шаблону, например jinja2
        yield """
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
        </script>
        """
        
        from db import get_all_command_name_by_description

        table_command = '<table style="width: 50%;">'
        table_command += '<tr><th>Команда</th><th>Описание</th></tr>'

        for name, description in get_all_command_name_by_description().items():
            row = '<tr><td>{}</td><td>{}</td></tr>'.format(name, description)
            table_command += row

        table_command += '</table>'

        yield table_command

        yield """
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


if __name__ == '__main__':
    # Set port
    cherrypy.config.update({'server.socket_port': 9090})

    # Autoreload off
    cherrypy.config.update({'engine.autoreload.on': False})

    cherrypy.quickstart(Root())
