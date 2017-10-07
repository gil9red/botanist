#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def hex2str(hex_string, encoding='cp1251'):
    items = []

    for i in range(0, len(hex_string), 2):
        hex2 = hex_string[i] + hex_string[i + 1]
        char = int(hex2, 16)
        items.append(char)

    return bytes(items).decode(encoding)


def str2hex(text, encoding='cp1251'):
    items = []

    for c in text.encode(encoding):
        # 'P' -> 0x50 -> 50
        hex_char = hex(c)[2:].upper()
        items.append(hex_char)

    return ''.join(items)


if __name__ == '__main__':
    assert hex2str("504F53542068747470733A") == "POST https:"
    assert str2hex(hex2str("504F53542068747470733A")) == "504F53542068747470733A"

    assert str2hex("POST https:") == "504F53542068747470733A"
    assert hex2str(str2hex("POST https:")) == "POST https:"

    assert str2hex("Привет мир!") == "CFF0E8E2E5F220ECE8F021"
    assert hex2str(str2hex("Привет мир!")) == "Привет мир!"

    assert hex2str("CFF0E8E2E5F220ECE8F021") == "Привет мир!"
    assert str2hex(hex2str("CFF0E8E2E5F220ECE8F021")) == "CFF0E8E2E5F220ECE8F021"

    hex_text = "504F53542068747470733A"
    text = hex2str(hex_text)
    print('"{}"'.format(text))

    text = "POST https:"
    hex_text = str2hex(text)
    print(hex_text)
