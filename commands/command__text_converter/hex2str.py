#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/6c0781de66aec4727616a06f536bcf052455cc88/hex2str/hex2str.py


def hex2str(hex_string: str, encoding='utf-8') -> str:
    data = bytes.fromhex(hex_string)
    return str(data, encoding)


def str2hex(text: str, encoding='utf-8', upper=True) -> str:
    hex_text = bytes(text, encoding).hex()
    if upper:
        hex_text = hex_text.upper()

    return hex_text


if __name__ == '__main__':
    assert hex2str("504F53542068747470733A") == "POST https:"
    assert str2hex(hex2str("504F53542068747470733A")) == "504F53542068747470733A"
    assert str2hex(hex2str("504F53542068747470733A"), upper=False) == "504f53542068747470733a"
    assert str2hex("POST https:") == "504F53542068747470733A"
    assert hex2str(str2hex("POST https:")) == "POST https:"
    assert hex2str(str2hex("Привет мир!")) == "Привет мир!"
    assert hex2str(str2hex("⌚⏰☀☁☔☺")) == "⌚⏰☀☁☔☺"

    hex_text = "504F53542068747470733A"
    text = hex2str(hex_text)
    print('"{}"'.format(text))

    text = "POST https:"
    hex_text = str2hex(text)
    print(hex_text)
