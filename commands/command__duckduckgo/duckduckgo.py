# duckduckgo.py - Library for querying the DuckDuckGo API
#
# Copyright (c) 2010 Michael Stephens <me@mikej.st>
# Copyright (c) 2012-2013 Michael Smith <crazedpsyc@gshellz.org>
# Copyright (c) 2017 Ilya Petrash aka gil9red <ilya.petrash@inbox.ru>
#
# See LICENSE for terms of usage, modification and redistribution.

# SOURCE: https://github.com/crazedpsyc/python-duckduckgo/blob/master/duckduckgo.py


import requests


__version__ = 0.243


def query(query, useragent='python-duckduckgo ' + str(__version__), safesearch=True, html=False, meanings=True,
          **kwargs):
    """
    Query DuckDuckGo, returning a Results object.

    Here's a query that's unlikely to change:

    >>> result = query('1 + 1')
    >>> result.type
    'nothing'
    >>> result.answer.text
    '1 + 1 = 2'
    >>> result.answer.type
    'calc'

    Keword arguments:
    useragent: UserAgent to use while querying. Default: "python-duckduckgo <__version__>" (str)
    safesearch: True for on, False for off. Default: True (bool)
    html: True to allow HTML in output. Default: False (bool)
    meanings: True to include disambiguations in results (bool)
    Any other keyword arguments are passed directly to DuckDuckGo as URL params.
    """

    safesearch = '1' if safesearch else '-1'
    html = '0' if html else '1'
    meanings = '0' if meanings else '1'
    params = {
        'q': query,
        'o': 'json',
        'kp': safesearch,
        'no_redirect': '1',
        'no_html': html,
        'd': meanings,
    }
    params.update(kwargs)

    rs = requests.get('http://api.duckduckgo.com/', params=params, headers={'User-Agent': useragent})
    json = rs.json()

    return Results(json)


class Results(object):
    def __init__(self, json):
        self.type = {
            'A': 'answer',
            'D': 'disambiguation',
            'C': 'category',
            'N': 'name',
            'E': 'exclusive',
            '': 'nothing'
        }.get(json.get('Type', ''), '')

        self.json = json
        self.api_version = None  # compat

        self.heading = json.get('Heading', '')

        self.results = [Result(elem) for elem in json.get('Results', [])]
        self.related = [Result(elem) for elem in json.get('RelatedTopics', [])]

        self.abstract = Abstract(json)
        self.redirect = Redirect(json)
        self.definition = Definition(json)
        self.answer = Answer(json)

        self.image = Image({'Result': json.get('Image', '')})


class Abstract(object):
    def __init__(self, json):
        self.html = json.get('Abstract', '')
        self.text = json.get('AbstractText', '')
        self.url = json.get('AbstractURL', '')
        self.source = json.get('AbstractSource')


class Redirect(object):
    def __init__(self, json):
        self.url = json.get('Redirect', '')


class Result(object):
    def __init__(self, json):
        self.topics = json.get('Topics', [])
        if self.topics:
            self.topics = [Result(t) for t in self.topics]
            return

        self.html = json.get('Result')
        self.text = json.get('Text')
        self.url = json.get('FirstURL')

        icon_json = json.get('Icon')
        if icon_json is not None:
            self.icon = Image(icon_json)
        else:
            self.icon = None


class Image(object):
    def __init__(self, json):
        self.url = json.get('Result')
        self.height = json.get('Height', None)
        self.width = json.get('Width', None)


class Answer(object):
    def __init__(self, json):
        self.text = json.get('Answer')
        self.type = json.get('AnswerType', '')


class Definition(object):
    def __init__(self, json):
        self.text = json.get('Definition', '')
        self.url = json.get('DefinitionURL')
        self.source = json.get('DefinitionSource')


def get_zci(q, web_fallback=True, priority=('answer', 'abstract', 'related.0', 'definition'), urls=True,
            on_no_results='Sorry, no results.', **kwargs):
    """
    A helper method to get a single (and hopefully the best) ZCI result.
    priority=list can be used to set the order in which fields will be checked for answers.
    Use web_fallback=True to fall back to grabbing the first web result.
    passed to query. This method will fall back to 'Sorry, no results.'
    if it cannot find anything.
    """

    ddg = query('\\' + q, **kwargs)
    response = ''

    for p in priority:
        ps = p.split('.')
        type = ps[0]
        result = getattr(ddg, type)

        index = int(ps[1]) if len(ps) > 1 else None
        if index is not None:
            if not hasattr(result, '__getitem__'):
                raise TypeError('%s field is not indexable' % type)

            result = result[index] if len(result) > index else None

        if not result:
            continue

        if hasattr(result, 'text'):
            if result.text:
                response = result.text

                if urls and hasattr(result, 'url') and result.url:
                    response += ' (%s)' % result.url

        elif result.topics:
            result = result.topics[0]
            if result.text:
                response = result.text

                if urls and hasattr(result, 'url') and result.url:
                    response += ' (%s)' % result.url

        if response:
            break

    # if there still isn't anything, try to get the first web result
    if not response and web_fallback:
        if ddg.redirect.url:
            response = ddg.redirect.url

    # final fallback
    if not response:
        response = on_no_results

    return response


# TODO: на основе get_zci и query_result сделать функцию, возвращающую один результат
#       в виде словаря с полями: text, url и img_url
# TODO: добавить аргумент lang и его значение подставять в kad
# TODO: добавить примеры значений lang/kad


if __name__ == '__main__':
    command = 'metallica'
    query_result = query(command, kad='ru_RU')
    print('"{}" -> {}'.format(command, query_result.json))

    command = 'metallica'
    query_result = query(command)
    print('"{}" -> {}'.format(command, query_result.json))
