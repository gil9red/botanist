#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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


# Выполнение
init_db()
