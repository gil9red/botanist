#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Maia'


import requests
from lxml import etree

def horoscope():
    url = "http://www.hyrax.ru/cgi-bin/bn_xml.cgi"
    rs = requests.get(url)
    root = etree.XML(rs.read())

    for item in root:
        print(item.xpath('child: description/ text'))

