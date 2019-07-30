# -*- coding: utf-8 -*-

"""This module allows to check Java code vulnerabilities."""

# standard imports
import re
from typing import Dict, List

# 3rd party imports
from pyparsing import (CaselessKeyword, Word, Literal, Optional, alphas,
                       alphanums, Suppress, nestedExpr, javaStyleComment,
                       QuotedString, oneOf, Keyword, MatchFirst, delimitedList,
                       ZeroOrMore, Empty)

# local imports
from fluidasserts import Result
from fluidasserts import LOW, MEDIUM
from fluidasserts import OPEN, CLOSED
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.decorators import track, level, notify, api


LANGUAGE_SPECS = {
    'extensions': ('java',),
    'block_comment_start': '/*',
    'block_comment_end': '*/',
    'line_comment': ('//',)
}  # type: dict


# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')
# Var$_123
L_VAR_NAME = Word(alphas + '$_', alphanums + '$_')
# Class$_123.property1.property1.value
L_VAR_CHAIN_NAME = delimitedList(L_VAR_NAME, delim='.', combine=True)


def _get_block(file_lines: list, line: int) -> str:
    """
    Return a Java block of code beginning in line.

    :param file_lines: Lines of code
    :param line: First line of block
    """
    return '\n'.join(file_lines[line - 1:])


def _declares_catch_for_exceptions(
        java_dest: str,
        exceptions_list: list,
        msgs: Dict[str, str],
        exclude: list = None) -> tuple:
    """Search for the declaration of catch for the given exceptions."""
    any_exception = L_VAR_CHAIN_NAME
    provided_exception = MatchFirst(
        [Keyword(exception) for exception in exceptions_list])

    exception_group = delimitedList(expr=any_exception, delim='|')
    exception_group.addCondition(
        # Ensure that at least one exception in the group is the provided one
        lambda tokens: any(provided_exception.matches(tok) for tok in tokens))

    grammar = Suppress(Keyword('catch')) + nestedExpr(
        opener='(', closer=')', content=(
            exception_group + Suppress(Optional(L_VAR_NAME))))
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW)
def has_generic_exceptions(java_dest: str, exclude: list = None) -> Result:
    """
    Search for generic exceptions in a Java source file or package.

    See `CWE-396 <https://cwe.mitre.org/data/definitions/396.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _declares_catch_for_exceptions(
        java_dest=java_dest,
        exceptions_list=[
            'Exception',
            'lang.Exception',
            'java.lang.Exception'],
        msgs={
            OPEN: 'Code declares a "catch" for generic exceptions',
            CLOSED: 'Code does not declare "catch" for generic exceptions',
        },
        exclude=exclude)


@api(risk=LOW)
def uses_catch_for_null_pointer_exception(
        java_dest: str, exclude: list = None) -> Result:
    """
    Search for the use of NullPointerException "catch" in a path.

    See `CWE-395 <https://cwe.mitre.org/data/definitions/395.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _declares_catch_for_exceptions(
        java_dest=java_dest,
        exceptions_list=[
            'NullPointerException',
            'lang.NullPointerException',
            'java.lang.NullPointerException'],
        msgs={
            OPEN: ('Code uses NullPointerException '
                   'Catch to Detect NULL Pointer Dereference'),
            CLOSED: ('Code does not use NullPointerException '
                     'Catch to Detect NULL Pointer Dereference'),
        },
        exclude=exclude)


@api(risk=LOW)
def uses_catch_for_runtime_exception(
        java_dest: str, exclude: list = None) -> Result:
    """
    Search for the use of RuntimeException "catch" in a path.

    See `CWE-544 <https://cwe.mitre.org/data/definitions/544.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _declares_catch_for_exceptions(
        java_dest=java_dest,
        exceptions_list=[
            'RuntimeException',
            'lang.RuntimeException',
            'java.lang.RuntimeException'],
        msgs={
            OPEN: ('Code declares a catch for RuntimeException '
                   'to handle programming mistakes '
                   'instead of prevent them by coding defensively'),
            CLOSED: 'Code does not declare a catch for RuntimeException',
        },
        exclude=exclude)


@api(risk=LOW)
def uses_print_stack_trace(java_dest: str, exclude: list = None) -> Result:
    """
    Search for ``printStackTrace`` calls in a path.

    See `CWE-209 <https://cwe.mitre.org/data/definitions/209.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    grammar = '.' + Keyword('printStackTrace')
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code uses Throwable.printStackTrace() method',
            CLOSED: 'Code does not use Throwable.printStackTrace() method'
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW)
def swallows_exceptions(java_dest: str, exclude: list = None) -> Result:
    """
    Search for ``catch`` blocks that are empty or only have comments.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-391 <https://cwe.mitre.org/data/definitions/391.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = Suppress(Keyword('catch')) + nestedExpr(opener='(', closer=')') \
        + nestedExpr(opener='{', closer='}', content=~Empty())
    grammar.ignore(javaStyleComment)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code has empty "catch" blocks',
            CLOSED: 'Code does not have empty "catch" blocks',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW)
def does_not_handle_exceptions(java_dest: str,
                               should_have: List[str],
                               use_regex: bool = False,
                               exclude: List[str] = None) -> Result:
    """
    Search for ``catch`` blocks that do not handle the exception.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-755 <https://cwe.mitre.org/data/definitions/755.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param should_have: List of expected exception handlers.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    if not use_regex:
        should_have = list(map(re.escape, should_have))
    should_have_regexps = tuple(re.compile(sh) for sh in should_have)

    grammar = Suppress(Keyword('catch') + nestedExpr(opener='(', closer=')')) \
        + nestedExpr(opener='{', closer='}')
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_CHAR)
    grammar.ignore(L_STRING)
    grammar.addCondition(
        lambda x: not any(shr.search(str(x)) for shr in should_have_regexps))

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code has "catch" blocks that do not handle its exceptions',
            CLOSED: 'All "catch" blocks in code handles its exceptions',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@notify
@level('low')
@track
def has_switch_without_default(java_dest: str, exclude: list = None) -> bool:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    switch = Keyword('switch') + nestedExpr(opener='(', closer=')')
    switch_line = Optional(Literal('}')) + switch + Optional(Literal('{'))

    try:
        switches = lang.check_grammar(switch_line, java_dest, LANGUAGE_SPECS,
                                      exclude)
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=java_dest))
        return False
    if not switches:
        show_close('Code does not have switches',
                   details=dict(code_dest=java_dest))
        return False

    switch_block = Suppress(switch) + nestedExpr(opener='{', closer='}')
    switch_block.ignore(javaStyleComment)
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
                   details=dict(file=java_dest,
                                fingerprint=get_sha256(java_dest)))
        return False

    show_open('Code does not have "switch" with "default" clause',
              details=dict(matched=vulns,
                           total_vulns=len(vulns)))
    return True


@api(risk=LOW)
def has_insecure_randoms(java_dest: str, exclude: list = None) -> Result:
    r"""
    Check if code uses insecure random generators.

    - ``java.util.Random()``.
    - ``java.lang.Math.random()``.

    See `REQ.224 <https://fluidattacks.com/web/rules/224/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    _java = Keyword('java')
    _util = Keyword('util')
    _lang = Keyword('lang')
    _math = Keyword('Math')
    _import = Keyword('import')
    _random_minus = Keyword('random')
    _random_mayus = Keyword('Random')
    _args = nestedExpr()

    insecure_randoms = MatchFirst([
        # util.Random()
        _util + '.' + _random_mayus + _args,
        # Math.random()
        _math + '.' + _random_minus + _args,
        # import java.util.Random
        _import + _java + '.' + _util + '.' + _random_mayus,
        # import java.lang.Math.random
        _import + _java + '.' + _lang + '.' + _math + '.' + _random_minus,
    ])
    insecure_randoms.ignore(javaStyleComment)
    insecure_randoms.ignore(L_CHAR)
    insecure_randoms.ignore(L_STRING)

    return lang.generic_method(
        path=java_dest,
        gmmr=insecure_randoms,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code uses insecure random generators',
            CLOSED: 'Code does not use insecure random generators',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@notify
@level('low')
@track
def has_if_without_else(java_dest: str, exclude: list = None) -> bool:
    r"""
    Check if all ``if``\ s have an ``else`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    args = nestedExpr(opener='(', closer=')')

    if_ = Keyword('if') + args
    if_line = Optional('}') + if_ + Optional('{')

    try:
        conds = lang.check_grammar(if_line, java_dest, LANGUAGE_SPECS, exclude)
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(code_dest=java_dest))
        return False
    else:
        if not conds:
            show_close('Code does not use "if" statements',
                       details=dict(code_dest=java_dest))
            return False

    block = nestedExpr(opener='{', closer='}')

    if_block = if_ + block
    else_if_block = Keyword('else') + Keyword('if') + args + block
    else_block = Keyword('else') + block

    cond_block = \
        Suppress(if_block + ZeroOrMore(else_if_block)) + Optional(else_block)
    cond_block.ignore(javaStyleComment)
    cond_block.ignore(L_CHAR)
    cond_block.ignore(L_STRING)

    vulns = {}
    for code_file, val in conds.items():
        vulns.update(lang.block_contains_empty_grammar(cond_block,
                                                       code_file, val['lines'],
                                                       _get_block))
    if not vulns:
        show_close('Code has "if" with "else" clause',
                   details=dict(file=java_dest,
                                fingerprint=get_sha256(java_dest)))
    else:
        show_open('Code has "if" without "else" clause',
                  details=dict(matched=vulns,
                               total_vulns=len(vulns)))
        return True
    return False


def _uses_insecure_cipher(java_dest: str, algorithm: tuple,
                          exclude: list = None) -> bool:
    """Check if code uses an insecure cipher algorithm."""
    method = 'Cipher.getInstance("{}")'.format(algorithm.upper())
    op_mode = '/' + oneOf('CBC ECB', caseless=True)
    padding = '/' + oneOf('NoPadding PKCS5Padding', caseless=True)
    algorithm = '"' + CaselessKeyword(algorithm) + Optional(
        op_mode + Optional(padding)) + '"'

    grammar = Suppress(Keyword('Cipher') + '.' + Keyword('getInstance')) + \
        nestedExpr()
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the provided algorithm
        lambda tokens: tokens.asList() and any(
            algorithm.matches(tok) for tok in tokens[0]))

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: f'Code uses {method} method',
            CLOSED: f'Code does not use {method} method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


def _uses_insecure_hash(java_dest: str, algorithm: tuple,
                        exclude: list = None) -> bool:
    """Check if code uses an insecure hashing algorithm."""
    method = f'MessageDigest.getInstance("{algorithm.upper()}")'
    tk_mess_dig = CaselessKeyword('messagedigest')
    tk_get_inst = CaselessKeyword('getinstance')
    tk_alg = Literal('"') + CaselessKeyword(algorithm.lower()) + Literal('"')
    tk_params = Literal('(') + tk_alg + Literal(')')
    instance = tk_mess_dig + Literal('.') + tk_get_inst + tk_params

    return lang.generic_method(
        path=java_dest,
        gmmr=instance,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: f'Code uses {method} method',
            CLOSED: f'Code does not use {method} method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=MEDIUM)
def uses_insecure_cipher(java_dest: str, algorithm: Result,
                         exclude: list = None) -> bool:
    """
    Check if code uses an insecure cipher algorithm.

    See `REQ.148 <https://fluidattacks.com/web/rules/148/>`_.
    See `REQ.149 <https://fluidattacks.com/web/rules/149/>`_.

    :param java_dest: Path to a Java source file or package.
    :param algorithm: Insecure algorithm.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _uses_insecure_cipher(java_dest, algorithm, exclude)


@api(risk=MEDIUM)
def uses_insecure_hash(java_dest: str, algorithm: Result,
                       exclude: list = None) -> bool:
    """
    Check if code uses an insecure hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param algorithm: Insecure algorithm.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _uses_insecure_hash(java_dest, algorithm, exclude)


@api(risk=MEDIUM)
def uses_md5_hash(java_dest: str, exclude: list = None) -> Result:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _uses_insecure_hash(java_dest, 'md5', exclude)


@api(risk=MEDIUM)
def uses_sha1_hash(java_dest: str, exclude: list = None) -> Result:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _uses_insecure_hash(java_dest, 'sha-1', exclude)


@api(risk=MEDIUM)
def uses_des_algorithm(java_dest: str, exclude: list = None) -> Result:
    """
    Check if code uses DES as encryption algorithm.

    See `REQ.149 <https://fluidattacks.com/web/rules/149/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    return _uses_insecure_cipher(java_dest, 'DES', exclude)


@api(risk=LOW)
def has_log_injection(java_dest: str, exclude: list = None) -> Result:
    """
    Search code injection.

    Check if the code does not neutralize or incorrectly neutralizes
    output that is written to logs.

    See `CWE-117 <https://cwe.mitre.org/data/definitions/117.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    log_variable = CaselessKeyword('log')
    log_level = oneOf('trace debug info warn error fatal')

    log_object = log_variable + Literal('.') + log_level

    tk_string = QuotedString('"')
    tk_var = Word(alphanums)

    grammar = log_object + Literal('(') + tk_string + Literal('+') + tk_var

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code allows logs injection',
            CLOSED: 'Code does not allow logs injection',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW)
def uses_system_exit(java_dest: str, exclude: list = None) -> Result:
    """
    Search for ``System.exit`` calls in a  or package.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    method = 'System.exit'
    grammar = Literal(method)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: f'Code uses {method} method',
            CLOSED: f'Code does not use {method} method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)
