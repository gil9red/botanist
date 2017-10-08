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


def create_connect():
    import sqlite3
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

                CONSTRAINT name_guid UNIQUE (guid)
            );
            
            CREATE TABLE IF NOT EXISTS Command (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                uri TEXT NOT NULL,
                description TEXT NOT NULL,
                server_guid TEXT NOT NULL
            );
            
        ''')

        connect.commit()


def get_commands() -> [(str, str, str)]:
    with create_connect() as connect:
        items = connect.execute('''
            SELECT Command.name, Command.description, Server.url || Command.uri 
            FROM Command, Server 
            WHERE Command.server_guid = Server.guid 
            ORDER BY Command.name
        ''').fetchall()

        return items


def get_all_command_name_by_description() -> {str: str}:
    return {name: description for name, description, _ in get_commands()}


def get_all_command_name_by_url() -> {str: str}:
    return {name: url for name, _, url in get_commands()}


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
                'INSERT INTO Server (name, guid, url) VALUES (?, ?, ?)', (server.name, server.guid, server.url)
            )

        # Иначе, обновляем
        else:
            connect.execute('UPDATE Server SET name=?, url=? WHERE guid=?', (server.name, server.url, server.guid))

        # Очищение списка комманд
        connect.execute("DELETE FROM Command WHERE server_guid = ?", (server.guid,))

        # Заполнение команд сервера
        for command in server.command_list:
            connect.execute(
                "INSERT INTO Command (name, uri, description, server_guid) VALUES (?, ?, ?, ?)",
                (command.name, command.uri, command.description, server.guid,)
            )

        connect.commit()


# Выполнение
init_db()
