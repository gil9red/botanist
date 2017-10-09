#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        import sys
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def make_backslashreplace_console():
    # При выводе юникодных символов в консоль винды
    # Возможно, не только для винды, но и для любой платформы стоит использовать
    # эту настройку -- мало какие проблемы могут встретиться
    import sys
    if sys.platform == 'win32':
        import codecs

        try:
            sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
            sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')

        except AttributeError:
            # ignore "AttributeError: '_io.BufferedWriter' object has no attribute 'encoding'"
            pass


TYPE_TEXT = 'text'
TYPE_IMAGE = 'image'
TYPE_GIF = 'gif'
TYPE_LIST_IMAGE = 'list_image'
