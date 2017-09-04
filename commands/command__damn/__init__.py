#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from commands.command__damn.damn import damn

# NOTE: for test
# def damn(name):
#     if not name:
#         return
#
#     return name.upper()


def execute(command):
    return damn(command)
