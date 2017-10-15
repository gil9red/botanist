#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import typing

DB_FILE_NAME = 'database.sqlite'

# Установка полного пути к файлу базы данных, так чтобы он был
# в той же папке что текущий файл
import os
dir = os.path.dirname(__file__)
file_name = os.path.join(dir, DB_FILE_NAME)
FULL_DB_FILE_NAME = os.path.abspath(file_name)


import sqlite3


def create_connect():
    return sqlite3.connect(FULL_DB_FILE_NAME)


def init_db():
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.executescript('''
            CREATE TABLE IF NOT EXISTS Server (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                guid TEXT NOT NULL,
                url TEXT NOT NULL,
                
                -- Полный путь к файлу сервера
                file_name TEXT NOT NULL,
                
                -- Дата последнего запроса к серверу
                datetime_last_request TEXT,
                
                -- Доступность
                availability BOOLEAN DEFAULT 0,

                -- Время последней доступности
                datetime_last_availability TEXT,

                CONSTRAINT name_guid UNIQUE (guid)
            );
            
            CREATE TABLE IF NOT EXISTS Command (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                uri TEXT NOT NULL,
                description TEXT NOT NULL,
                priority INTEGER NOT NULL,
                server_guid TEXT NOT NULL
            );
            
        ''')

        connect.commit()


# TODO: завести в базе статистику команд таблицу в которой будет инфа о времени выполнения и названии команды
# TODO: при сборе статистики думаю желательно знать о количестве команд, о том сколько из них провалилось, выполнилось
def add_statistics():
    pass


def get_commands() -> [(str, str, str)]:
    with create_connect() as connect:
        items = connect.execute('''
            SELECT Command.name, Command.description, Server.url || Command.uri 
            FROM Command, Server 
            WHERE Command.server_guid = Server.guid 
            
            -- Сортировка по приоритету по убыванию и сортировка по названию по возрастанию
            ORDER BY Command.priority desc, Command.name asc

        ''').fetchall()

        return items


def get_all_command_name_by_description() -> typing.Dict[str, str]:
    from collections import OrderedDict
    items = OrderedDict()

    for name, description, _ in get_commands():
        items[name] = description

    return items


def get_all_command_name_by_url() -> typing.Dict[str, str]:
    from collections import OrderedDict
    items = OrderedDict()

    for name, _, url in get_commands():
        items[name] = url

    return items


def get_execute_command_list_url_server(guid: str) -> [typing.Union[str, None]]:
    with create_connect() as connect:
        url_list = connect.execute('''
            SELECT Server.url || Command.uri 
            FROM Command, Server 
            WHERE Command.server_guid = :guid AND Server.guid = :guid
            ''', {'guid': guid}

        ).fetchall()

        return [x for x, in url_list]


def get_execute_command_url_server(guid: str) -> typing.Union[str, None]:
    url_list = get_execute_command_list_url_server(guid)
    if not url_list:
        return

    return url_list[0]


def get_all_server() -> typing.List[dict]:
    with create_connect() as connect:
        connect.row_factory = sqlite3.Row

        return [dict(x) for x in connect.execute('SELECT * FROM Server').fetchall()]


def get_commands_by_guid(guid: str) -> [(str, str, str)]:
    with create_connect() as connect:
        items = connect.execute('''
            SELECT Command.name, Command.description, Server.url || Command.uri 
            FROM Command, Server 
            WHERE Command.server_guid = :guid and Server.guid = :guid

            -- Сортировка по приоритету по убыванию и сортировка по названию по возрастанию
            ORDER BY Command.priority desc, Command.name asc

        ''', {'guid': guid}).fetchall()

        return items


def get_all_server_with_commands() -> typing.List[dict]:
    server_list = []

    for server in get_all_server():
        server['command_list'] = get_commands_by_guid(server['guid'])
        server_list.append(server)

    return server_list


def get_url_server(guid: str) -> typing.Union[str, None]:
    with create_connect() as connect:
        url = connect.execute('SELECT Server.url FROM Server WHERE Server.guid = :guid ', {'guid': guid}).fetchone()
        if url is None:
            return

        return url[0]


def get_url_coordinator() -> typing.Union[str, None]:
    return get_execute_command_url_server('B57B73C8F8D442C48EDAFC951963D7A5')


def fill_server_info(server):
    with create_connect() as connect:
        # Если не существует, добавляем запись
        exist = connect.execute("SELECT 1 FROM Server WHERE guid = ?", (server.guid,)).fetchone()
        if not exist:
            connect.execute(
                'INSERT INTO Server (name, guid, url, file_name) VALUES (?, ?, ?, ?)',
                (server.name, server.guid, server.url, server.file_name)
            )

        # Иначе, обновляем
        else:
            connect.execute('UPDATE Server SET name=?, url=?, file_name=? WHERE guid=?',
                            (server.name, server.url, server.file_name, server.guid))

        # Очищение списка комманд
        connect.execute("DELETE FROM Command WHERE server_guid = ?", (server.guid,))

        # Заполнение команд сервера
        for command in server.command_list:
            connect.execute(
                "INSERT INTO Command (name, uri, description, priority, server_guid) VALUES (?, ?, ?, ?, ?)",
                (command.name, command.uri, command.description, command.priority, server.guid,)
            )

        connect.commit()


def update_datetime_last_request(server):
    with create_connect() as connect:
        sql = """
            UPDATE Server 
            SET 
                datetime_last_request=strftime('%d/%m/%Y %H:%M:%S', datetime('now', 'localtime')) 
            WHERE guid=?
        """
        connect.execute(sql, (server.guid,))
        connect.commit()


def update_availability(server_guid: str, availability: bool):
    with create_connect() as connect:
        if availability:
            sql = """
                UPDATE Server 
                SET 
                    availability=1, 
                    datetime_last_availability=strftime('%d/%m/%Y %H:%M:%S', datetime('now', 'localtime'))
                WHERE guid=?
            """
        else:
            sql = "UPDATE Server SET availability=0 WHERE guid=?"

        connect.execute(sql, (server_guid,))
        connect.commit()


# Выполнение
init_db()


if __name__ == '__main__':
    for server in get_all_server_with_commands():
        print(server)

        for command in server['command_list']:
            print(f'    {command}')

        print()
