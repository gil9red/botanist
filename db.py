#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


DB_FILE_NAME = 'database.sqlite'


def create_connect():
    import sqlite3
    return sqlite3.connect(DB_FILE_NAME)
