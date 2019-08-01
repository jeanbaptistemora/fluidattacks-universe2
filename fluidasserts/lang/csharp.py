# -*- coding: utf-8 -*-

"""This module allows to check ``C#`` code vulnerabilities."""

# standard imports
from typing import Dict, List

# 3rd party imports
from pyparsing import (CaselessKeyword, Word, Literal, Optional, alphas,
                       alphanums, Suppress, nestedExpr, cppStyleComment,
                       SkipTo, Keyword, MatchFirst, QuotedString,
                       delimitedList)

# local imports
from fluidasserts import Result
from fluidasserts import LOW
from fluidasserts import OPEN, CLOSED
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.decorators import track, level, notify, api


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


def _get_block(file_lines: list, line: int) -> str:
    """
    Return a C# block of code beginning in line.

    :param file_lines: Lines of code
    :param line: First line of block
    """
    return '\n'.join(file_lines[line - 1:])


def _get_block_as_one_liner(file_lines, line) -> str:
    """
    Return a C# block of code beginning in line.

    :param file_lines: Lines of code
    :param line: First line of block
    """
    return "".join(file_lines[line - 1:])


def _declares_catch_for_exceptions(
        csharp_dest: str,
        exceptions_list: List[str],
        msgs: Dict[str, str],
        exclude: list = None) -> tuple:
    """Search for the declaration of catch for the given exceptions."""
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list])

    grammar = Keyword('catch') + nestedExpr(
        opener='(', closer=')', content=(
            provided_exception + Optional(L_VAR_NAME)))
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=csharp_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW)
def has_generic_exceptions(csharp_dest: str, exclude: list = None) -> Result:
    """
    Search for generic exceptions in a C# source file or package.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
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
        msgs={
            OPEN: 'Code declares a "catch" for generic exceptions',
            CLOSED: 'Code does not declare "catch" for generic exceptions',
        },
        exclude=exclude)


@notify
@level('low')
@track
def swallows_exceptions(csharp_dest: str, exclude: list = None) -> bool:
    """
    Search for ``catch`` blocks that are empty or only have comments.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_catch = CaselessKeyword('catch')
    tk_word = Word(alphas)
    parser_catch = (Optional(Literal('}')) + tk_catch + Literal('(') +
                    tk_word + Optional(Literal('(') + tk_word + Literal(')')) +
                    Optional(tk_word) + Literal(')'))
    empty_catch = (Suppress(parser_catch) +
                   nestedExpr(opener='{', closer='}')).ignore(cppStyleComment)

    result = False
    try:
        catches = lang.check_grammar(parser_catch, csharp_dest,
                                     LANGUAGE_SPECS, exclude)
        if not catches:
            show_close('Code does not have catches',
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        return False
    vulns = {}
    for code_file, val in catches.items():
        vulns.update(lang.block_contains_empty_grammar(
            empty_catch,
            code_file, val['lines'], _get_block_as_one_liner))
    if not vulns:
        show_close('Code does not have empty catches',
                   details=dict(file=csharp_dest,
                                fingerprint=get_sha256(csharp_dest)))
    else:
        show_open('Code has empty catches',
                  details=dict(matches=vulns, total_vulns=len(vulns)))
        result = True
    return result


@notify
@level('low')
@track
def has_switch_without_default(csharp_dest: str, exclude: list = None) -> bool:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    switch = Keyword('switch') + nestedExpr(opener='(', closer=')')
    switch_line = Optional('}') + switch + Optional('{')

    result = False
    try:
        switches = lang.check_grammar(switch_line, csharp_dest, LANGUAGE_SPECS,
                                      exclude)
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        return False
    else:
        if not switches:
            show_close('Code does not have switches',
                       details=dict(code_dest=csharp_dest))
            return False

    switch_block = Suppress(switch) + nestedExpr(opener='{', closer='}')
    switch_block.ignore(cppStyleComment)
    switch_block.ignore(L_CHAR)
    switch_block.ignore(L_STRING)

    vulns = {}
    for code_file, val in switches.items():
        vulns.update(lang.block_contains_grammar(
            switch_block,
            code_file, val['lines'],
            _get_block,
            should_not_have=r'(?:default\s*:)'))
    if not vulns:
        show_close('Code has "switch" with "default" clause',
                   details=dict(file=csharp_dest,
                                fingerprint=get_sha256(csharp_dest)))
    else:
        show_open('Code does not have "switch" with "default" clause',
                  details=dict(matched=vulns,
                               total_vulns=len(vulns)))
        result = True
    return result


@notify
@level('low')
@track
def has_insecure_randoms(csharp_dest: str, exclude: list = None) -> bool:
    """
    Check if code instantiates ``Random`` class.

    See `REQ.224 <https://fluidattacks.com/web/rules/224/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_new = Keyword('new')
    tk_var = Keyword('var')
    tk_equal = Literal('=')
    tk_params = nestedExpr()
    tk_random = Keyword('Random')
    tk_variable = Word(alphas + '_', alphanums + '_')

    instantiation = (tk_var | tk_random) + tk_variable + tk_equal + tk_new + \
        tk_random + Suppress(tk_params)

    result = False
    try:
        random_new = lang.check_grammar(instantiation, csharp_dest,
                                        LANGUAGE_SPECS, exclude)
        if not random_new:
            show_close('Code does not generate insecure random numbers',
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        result = False
    else:
        result = True
        show_open('Code generates insecure random numbers',
                  details=dict(matched=random_new,
                               total_vulns=len(random_new)))
    return result


@notify
@level('low')
@track
def has_if_without_else(csharp_dest: str, exclude: list = None) -> bool:
    r"""
    Check if all ``if``\ s have an ``else`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    tk_if = CaselessKeyword('if')
    tk_else = CaselessKeyword('else')
    block = nestedExpr(opener='{', closer='}')
    prsr_if = tk_if + nestedExpr() + block
    prsr_else = Suppress(tk_else) + (prsr_if | block)
    if_head = tk_if + nestedExpr() + Optional(Literal('{'))
    if_wout_else = (Suppress(prsr_if) + prsr_else).ignore(cppStyleComment)

    result = False
    try:
        conds = lang.check_grammar(if_head, csharp_dest,
                                   LANGUAGE_SPECS, exclude)
        if not conds:
            show_close('Code does not have conditionals',
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        return False
    vulns = {}
    for code_file, val in conds.items():
        vulns.update(lang.block_contains_empty_grammar(
            if_wout_else,
            code_file, val['lines'], _get_block_as_one_liner))
    if not vulns:
        show_close('Code has "if" with "else" clauses',
                   details=dict(file=csharp_dest,
                                fingerprint=get_sha256(csharp_dest)))
    else:
        show_open('Code does not have "if" with "else" clauses',
                  details=dict(matched=vulns,
                               total_vulns=len(vulns)))
        result = True
    return result


@notify
@level('medium')
@track
def uses_md5_hash(csharp_dest: str, exclude: list = None) -> bool:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    method = 'MD5.Create(), new MD5CryptoServiceProvider()'
    tk_md5 = CaselessKeyword('md5')
    tk_create = CaselessKeyword('create')
    tk_params = nestedExpr()
    fn_1 = tk_md5 + Literal('.') + tk_create + tk_params

    tk_new = CaselessKeyword('new')
    tk_md5cry = CaselessKeyword('MD5CryptoServiceProvider')
    tk_params = nestedExpr()
    fn_2 = tk_new + tk_md5cry + tk_params

    call_function = MatchFirst([fn_1, fn_2])

    result = False
    try:
        matches = lang.check_grammar(call_function, csharp_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code uses {} method'.format(method),
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        result = False
    else:
        result = True
        show_open('Code uses {} method'.format(method),
                  details=dict(matched=matches,
                               total_vulns=len(matches)))
    return result


@notify
@level('medium')
@track
def uses_sha1_hash(csharp_dest: str, exclude: list = None) -> bool:
    """
    Check if code uses SHA1 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    method = "new SHA1CryptoServiceProvider(), new SHA1Managed()"
    tk_new = CaselessKeyword('new')
    tk_sha1cry = CaselessKeyword('SHA1CryptoServiceProvider')
    tk_sha1man = CaselessKeyword('SHA1Managed')
    tk_params = nestedExpr()
    call_function = tk_new + MatchFirst([tk_sha1cry, tk_sha1man]) + tk_params

    result = False
    try:
        matches = lang.check_grammar(call_function, csharp_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code does not use {} method'.format(method),
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        return False
    else:
        result = True
        show_open('Code uses {} method'.format(method),
                  details=dict(matched=matches,
                               total_vulns=len(matches)))
    return result


@notify
@level('medium')
@track
def uses_ecb_encryption_mode(csharp_dest: str, exclude: list = None) -> bool:
    """
    Check if code uses ECB as encryption mode.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    method = "Mode = CipherMode.ECB"
    tk_eq = Literal('=')
    tk_obj = SkipTo(tk_eq)
    tk_cm = CaselessKeyword('ciphermode')
    tk_ecb = CaselessKeyword('ecb')
    call_function = tk_obj + tk_eq + tk_cm + Literal('.') + tk_ecb

    result = False
    try:
        matches = lang.check_grammar(call_function, csharp_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code does not use {} method'.format(method),
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        result = False
    else:
        result = True
        show_open('Code uses {} method'.format(method),
                  details=dict(matched=matches,
                               total_vulns=len(matches)))
    return result


@notify
@level('low')
@track
def uses_debug_writeline(csharp_dest: str, exclude: list = None) -> bool:
    """
    Check if code uses Debug.WriteLine method.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    method = "Debug.WriteLine"
    tk_debug = CaselessKeyword('debug')
    tk_wrilin = CaselessKeyword('writeline')
    call_function = tk_debug + Literal('.') + tk_wrilin

    result = False
    try:
        matches = lang.check_grammar(call_function, csharp_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code does not use {} method'.format(method),
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        result = False
    else:
        result = True
        show_open('Code uses {} method'.format(method),
                  details=dict(matched=matches,
                               total_vulns=len(matches)))
    return result


@notify
@level('low')
@track
def uses_console_writeline(csharp_dest: str, exclude: list = None) -> bool:
    """
    Check if code uses Console.WriteLine method.

    :param csharp_dest: Path to a C# source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    method = "Console.WriteLine"
    tk_console = CaselessKeyword('console')
    tk_wrilin = CaselessKeyword('writeline')
    call_function = tk_console + Literal('.') + tk_wrilin

    result = False
    try:
        matches = lang.check_grammar(call_function, csharp_dest,
                                     LANGUAGE_SPECS, exclude)
        if not matches:
            show_close('Code does not use {} method'.format(method),
                       details=dict(code_dest=csharp_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=csharp_dest))
        return False
    else:
        result = True
        show_open('Code uses {} method'.format(method),
                  details=dict(matched=matches,
                               total_vulns=len(matches)))
    return result
