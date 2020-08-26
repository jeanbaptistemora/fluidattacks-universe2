# -*- coding: utf-8 -*-

"""This module allows to check ``C#`` code vulnerabilities."""

# standard imports
from typing import Dict, List

# 3rd party imports
from pyparsing import (Word, Optional, alphas,
                       alphanums, Suppress, nestedExpr, cppStyleComment,
                       Keyword, MatchFirst, QuotedString,
                       delimitedList, Empty)

# local imports
from fluidasserts import LOW, MEDIUM, OPEN, CLOSED, SAST
from fluidasserts.lang import core
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api


LANGUAGE_SPECS = {
    'extensions': ('cs',),
    'block_comment_start': '/*',
    'block_comment_end': '*/',
    'line_comment': ('//',)
}  # type: dict


# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')
# _Var_123
L_VAR_NAME = Word(alphas + '_', alphanums + '_')
# Class_123.property1.property1.value
L_VAR_CHAIN_NAME = delimitedList(L_VAR_NAME, delim='.', combine=True)


def _declares_catch_for_exceptions(
        csharp_dest: str,
        exceptions_list: List[str],
        msgs: Dict[str, str],
        allow_empty: bool = False,
        exclude: list = None) -> tuple:
    """Search for the declaration of catch for the given exceptions."""
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list])

    grammar = Keyword('catch') + nestedExpr(
        opener='(', closer=')', content=(
            provided_exception + Optional(L_VAR_NAME)))
    if allow_empty:
        grammar = MatchFirst([
            Keyword('catch') + nestedExpr(opener='{', closer='}'),
            grammar.copy(),
        ])

    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_generic_exceptions(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Search for generic exceptions in a C# source file or package.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        csharp_dest=csharp_dest,
        exceptions_list=[
            'Exception',
            'ApplicationException',
            'SystemException',

            'System.Exception',
            'System.ApplicationException',
            'System.SystemException',
        ],
        allow_empty=True,
        msgs={
            OPEN: 'Code declares a "catch" for generic exceptions',
            CLOSED: 'Code does not declare "catch" for generic exceptions',
        },
        exclude=exclude)


@api(risk=LOW, kind=SAST)
def uses_catch_for_null_reference_exception(
        csharp_dest: str, exclude: list = None) -> tuple:
    """
    Search for the use of NullReferenceException "catch" in a path.

    See `CWE-395 <https://cwe.mitre.org/data/definitions/395.html>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _declares_catch_for_exceptions(
        csharp_dest=csharp_dest,
        exceptions_list=[
            'NullReferenceException',
            'system.NullReferenceException',
        ],
        msgs={
            OPEN: ('Code uses NullReferenceException '
                   'Catch to handle NULL Pointer Dereferences'),
            CLOSED: ('Code does not use NullPointerException '
                     'Catch to handle NULL Pointer Dereferences'),
        },
        exclude=exclude)


@api(risk=LOW, kind=SAST)
def swallows_exceptions(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``catch`` blocks that are empty or only have comments.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = Suppress(Keyword('catch')) \
        + Optional(nestedExpr(opener='(', closer=')')) \
        + nestedExpr(opener='{', closer='}', content=~Empty())
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has empty "catch" blocks',
            CLOSED: 'Code does not have empty "catch" blocks',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_switch_without_default(
        csharp_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_switch_without_default(
        csharp_dest, LANGUAGE_SPECS, exclude)


@api(risk=LOW, kind=SAST)
def has_insecure_randoms(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code instantiates ``Random`` class.

    See `REQ.224 <https://fluidattacks.com/web/rules/224/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    # module: System
    # secure versions: System.Security.Cryptography.RandomNumberGenerator
    #                  System.Security.Cryptography.RNGCryptoServiceProvider
    grammar = Keyword('new') + Optional(Keyword('System') + '.') + \
        Keyword('Random') + nestedExpr()
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code generates insecure random numbers',
            CLOSED: 'Code does not generate insecure random numbers',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_if_without_else(
        csharp_dest: str,
        conditions: list,
        use_regex: bool = False,
        exclude: list = None) -> tuple:
    r"""
    Check if all ``if``\ s have an ``else`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param conditions: List of texts between parentheses of the
                      `if (condition)` statement.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_if_without_else(
        csharp_dest, conditions, use_regex, LANGUAGE_SPECS, exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_md5_hash(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = MatchFirst([
        Keyword('MD5CryptoServiceProvider'),
        Keyword('MD5') + '.' + Keyword('Create')
    ]) + nestedExpr()
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses MD5 hash',
            CLOSED: 'Code does not use MD5 hash',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_sha1_hash(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses SHA1 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    methods = ('SHA1CryptoServiceProvider', 'SHA1Managed')
    grammar = MatchFirst(map(Keyword, methods)) + nestedExpr()
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses SHA1 hash',
            CLOSED: 'Code does not use SHA1 hash',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_ecb_encryption_mode(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses ECB as encryption mode.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Keyword('CipherMode') + '.' + Keyword('ECB')
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses CipherMode.ECB mode of operation',
            CLOSED: 'Code does not use CipherMode.ECB mode of operation',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def uses_debug_writeline(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses Debug.WriteLine method.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    methods = ('Write', 'WriteIf',
               'WriteLine', 'WriteLineIf',
               'Assert', 'Fail', 'Print')
    grammar = Keyword('Debug') + '.' + MatchFirst(map(Keyword, methods))
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses Debug.WriteLine method',
            CLOSED: 'Code does not use Debug.WriteLine method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def uses_console_writeline(csharp_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses Console.WriteLine method.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    methods = ('WriteLine', 'Write')
    grammar = Keyword('Console') + '.' + MatchFirst(map(Keyword, methods))
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses Console.WriteLine method',
            CLOSED: 'Code does not use Console.WriteLine method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)
