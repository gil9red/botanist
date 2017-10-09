#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import cherrypy


class Root:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def execute(self):
        rq = cherrypy.request.json
        print(rq)

        command = rq['command']

        from commands import execute
        rs = execute(command, raw=True)

        return rs

    @cherrypy.expose
    def index(self):
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
        
            function execute() {
                $.ajax({
                    type: 'POST',
                    url: "/execute",
                    contentType: "application/json",
                    dataType: "json",  // тип данных загружаемых с сервера
                    processData: false,
                    data: JSON.stringify({'command': $('#update_box').val()}),
                    
                    success: function(data) {
                        var json_str = JSON.stringify(data, undefined, 4);
                        console.log(json_str);
                        
                        json_str = syntaxHighlight(json_str);
                    
                        $('.result.show > pre').html(json_str);
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
                        $('.result.show > pre').html(msg);
                        $('.result.show').show();
                    },
                });
            }
        </script>
        """
        
        from db import get_all_command_name_by_description

        table_command = '<table>'
        table_command += '<tr><th>Команда</th><th>Описание</th></tr>'

        for name, description in get_all_command_name_by_description().items():
            row = '<tr><td>{}</td><td>{}</td></tr>'.format(name, description)
            table_command += row

        table_command += '</table>'

        yield table_command

        yield """
        <br>
        <input type='textbox' id='update_box' value='str2hex Привет Мир!' size='100' />
        <input type='submit' value='execute' onClick='execute(); return false' />
        
        <br>
        <div class="result show" style="display: none">
            <p>Result:</p>
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
