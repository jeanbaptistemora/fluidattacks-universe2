# -*- coding: utf-8 -*-

"""This module allows to check JavaScript code vulnerabilities."""

# standard imports
import re

# 3rd party imports
from pyparsing import (Suppress, nestedExpr, cppStyleComment,
                       MatchFirst, Keyword, Empty, QuotedString)

# local imports
from fluidasserts import LOW, MEDIUM, OPEN, CLOSED, SAST
from fluidasserts.lang import core
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api

LANGUAGE_SPECS = {
    'extensions': ('js', 'ts',),
    'block_comment_start': '/*',
    'block_comment_end': '*/',
    'line_comment': ('//',)
}  # type: dict


# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')
# Compiled regular expressions
RE_HAVES_DEFAULT = re.compile(r'(?:default\s*:)', flags=re.M)


@api(risk=LOW, kind=SAST)
def uses_console_log(js_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``console.log()`` calls in a JavaScript file or directory.

    :param js_dest: Path to a JavaScript source file or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Keyword('console') + '.' + Keyword('log') + nestedExpr()
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    return lang.generic_method(
        path=js_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses Console.log() method',
            CLOSED: 'Code does not use Console.log() method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_eval(js_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``eval()`` calls in a JavaScript file or directory.

    :param js_dest: Path to a JavaScript source file or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Keyword('eval') + nestedExpr()
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    return lang.generic_method(
        path=js_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses eval() method',
            CLOSED: 'Code does not use eval() method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def uses_localstorage(js_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``localStorage`` calls in a JavaScript source file or directory.

    :param js_dest: Path to a JavaScript source file or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Keyword('localStorage') + '.'
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    return lang.generic_method(
        path=js_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses window.localStorage method',
            CLOSED: 'Code does not use window.localStorage method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_insecure_randoms(js_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if code uses ``Math.Random()``\ .

    See `REQ.224 <https://fluidattacks.com/web/rules/224/>`_.

    :param js_dest: Path to a JavaScript source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Keyword('Math') + '.' + Keyword('random') + nestedExpr()
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    return lang.generic_method(
        path=js_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses Math.random() method',
            CLOSED: 'Code does not use Math.random() method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def swallows_exceptions(js_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``catch`` blocks that are empty or only have comments.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-391 <https://cwe.mitre.org/data/definitions/391.html>`_.

    :param js_dest: Path to a JavaScript source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    classic = Suppress(Keyword('catch')) + nestedExpr(opener='(', closer=')') \
        + nestedExpr(opener='{', closer='}', content=~Empty())

    modern = Suppress('.' + Keyword('catch')) + nestedExpr(
        opener='(', closer=')', content=~Empty())

    grammar = MatchFirst([classic, modern])
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    return lang.generic_method(
        path=js_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has empty "catch" blocks',
            CLOSED: 'Code does not have empty "catch" blocks',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_switch_without_default(js_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param js_dest: Path to a JavaScript source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    switch = Keyword('switch') + nestedExpr(opener='(', closer=')')
    grammar = Suppress(switch) + nestedExpr(opener='{', closer='}')
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    grammar.addCondition(lambda x: not RE_HAVES_DEFAULT.search(str(x)))

    return lang.generic_method(
        path=js_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code does not have "switch" with "default" clause',
            CLOSED: 'Code has "switch" with "default" clause',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_if_without_else(
        js_dest: str,
        conditions: list,
        use_regex: bool = False,
        exclude: list = None) -> tuple:
    r"""
    Check if all ``if``\ s have an ``else`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param js_dest: Path to a JavaScript source file or package.
    :param conditions: List of texts between parentheses of the
                      `if (condition)` statement.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_if_without_else(
        js_dest, conditions, use_regex, LANGUAGE_SPECS, exclude)
