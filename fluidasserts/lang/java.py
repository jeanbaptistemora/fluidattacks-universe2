# -*- coding: utf-8 -*-

"""This module allows to check Java code vulnerabilities."""

# standard imports
import re
from typing import Dict, List

# 3rd party imports
from pyparsing import (CaselessKeyword, Word, Literal, Optional, alphas,
                       alphanums, Suppress, nestedExpr, javaStyleComment,
                       QuotedString, oneOf, Keyword, MatchFirst, delimitedList,
                       Empty)

# local imports
from fluidasserts import LOW, MEDIUM, OPEN, CLOSED, SAST
from fluidasserts.lang import core
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api


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
        func=lang.parse,
        msgs=msgs,
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_generic_exceptions(java_dest: str, exclude: list = None) -> tuple:
    """
    Search for generic exceptions in a Java source file or package.

    See `CWE-396 <https://cwe.mitre.org/data/definitions/396.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
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


@api(risk=LOW, kind=SAST)
def uses_catch_for_null_pointer_exception(
        java_dest: str, exclude: list = None) -> tuple:
    """
    Search for the use of NullPointerException "catch" in a path.

    See `CWE-395 <https://cwe.mitre.org/data/definitions/395.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
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


@api(risk=LOW, kind=SAST)
def uses_catch_for_runtime_exception(
        java_dest: str, exclude: list = None) -> tuple:
    """
    Search for the use of RuntimeException "catch" in a path.

    See `CWE-544 <https://cwe.mitre.org/data/definitions/544.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
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


@api(risk=LOW, kind=SAST)
def uses_print_stack_trace(java_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``printStackTrace`` calls in a path.

    See `CWE-209 <https://cwe.mitre.org/data/definitions/209.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = '.' + Keyword('printStackTrace')
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses Throwable.printStackTrace() method',
            CLOSED: 'Code does not use Throwable.printStackTrace() method'
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def swallows_exceptions(java_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``catch`` blocks that are empty or only have comments.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-391 <https://cwe.mitre.org/data/definitions/391.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = Suppress(Keyword('catch')) + nestedExpr(opener='(', closer=')') \
        + nestedExpr(opener='{', closer='}', content=~Empty())
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has empty "catch" blocks',
            CLOSED: 'Code does not have empty "catch" blocks',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def does_not_handle_exceptions(java_dest: str,
                               should_have: List[str],
                               use_regex: bool = False,
                               exclude: List[str] = None) -> tuple:
    """
    Search for ``catch`` blocks that do not handle the exception.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-755 <https://cwe.mitre.org/data/definitions/755.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param should_have: List of expected exception handlers.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
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
        func=lang.parse,
        msgs={
            OPEN: 'Code has "catch" blocks that do not handle its exceptions',
            CLOSED: 'All "catch" blocks in code handles its exceptions',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_switch_without_default(java_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_switch_without_default(
        java_dest, LANGUAGE_SPECS, exclude)


@api(risk=LOW, kind=SAST)
def has_insecure_randoms(java_dest: str, exclude: list = None) -> tuple:
    r"""
    Check if code uses insecure random generators.

    - ``java.util.Random()``.
    - ``java.lang.Math.random()``.

    See `REQ.224 <https://fluidattacks.com/web/rules/224/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    _java = Keyword('java')
    _util = Keyword('util')
    _lang = Keyword('lang')
    _math = Keyword('Math')
    _import = Keyword('import')
    _random_minus = Keyword('random')
    _random_mayus = Keyword('Random')
    _args = nestedExpr()

    grammar = MatchFirst([
        # util.Random()
        _util + '.' + _random_mayus + _args,
        # Math.random()
        _math + '.' + _random_minus + _args,
        # import java.util.Random
        _import + _java + '.' + _util + '.' + _random_mayus,
        # import java.lang.Math.random
        _import + _java + '.' + _lang + '.' + _math + '.' + _random_minus,
    ])
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses insecure random generators',
            CLOSED: 'Code does not use insecure random generators',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_if_without_else(
        java_dest: str,
        conditions: list,
        use_regex: bool = False,
        exclude: list = None) -> tuple:
    r"""
    Check if all ``if``\ s have an ``else`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    :param java_dest: Path to a Java source file or package.
    :param conditions: List of texts between parentheses of the
                      `if (condition)` statement.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return core.generic_c_has_if_without_else(
        java_dest, conditions, use_regex, LANGUAGE_SPECS, exclude)


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
        func=lang.parse,
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
    grammar = tk_mess_dig + Literal('.') + tk_get_inst + tk_params
    grammar.ignore(javaStyleComment)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f'Code uses {method} method',
            CLOSED: f'Code does not use {method} method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_insecure_cipher(java_dest: str, algorithm: str,
                         exclude: list = None) -> bool:
    """
    Check if code uses an insecure cipher algorithm.

    See `REQ.148 <https://fluidattacks.com/web/rules/148/>`_.
    See `REQ.149 <https://fluidattacks.com/web/rules/149/>`_.

    :param java_dest: Path to a Java source file or package.
    :param algorithm: Insecure algorithm.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_cipher(java_dest, algorithm, exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_insecure_hash(java_dest: str, algorithm: str,
                       exclude: list = None) -> bool:
    """
    Check if code uses an insecure hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param algorithm: Insecure algorithm.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_hash(java_dest, algorithm, exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_md5_hash(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_hash(java_dest, 'md5', exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_sha1_hash(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses MD5 as hashing algorithm.

    See `REQ.150 <https://fluidattacks.com/web/rules/150/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_hash(java_dest, 'sha-1', exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_des_algorithm(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if code uses DES as encryption algorithm.

    See `REQ.149 <https://fluidattacks.com/web/rules/149/>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_insecure_cipher(java_dest, 'DES', exclude)


@api(risk=LOW, kind=SAST)
def has_log_injection(java_dest: str, exclude: list = None) -> tuple:
    """
    Search code injection.

    Check if the code does not neutralize or incorrectly neutralizes
    output that is written to logs.

    See `CWE-117 <https://cwe.mitre.org/data/definitions/117.html>`_.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    log_variable = CaselessKeyword('log')
    log_level = oneOf('trace debug info warn error fatal')

    log_object = log_variable + Literal('.') + log_level

    tk_string = QuotedString('"')
    tk_var = Word(alphanums)

    grammar = log_object + Literal('(') + tk_string + Literal('+') + tk_var
    grammar.ignore(javaStyleComment)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code allows logs injection',
            CLOSED: 'Code does not allow logs injection',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def uses_system_exit(java_dest: str, exclude: list = None) -> tuple:
    """
    Search for ``System.exit`` calls in a  or package.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    method = 'System.exit'
    grammar = Keyword('System') + '.' + Keyword('exit')
    grammar.ignore(javaStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f'Code uses {method} method',
            CLOSED: f'Code does not use {method} method',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_insecure_aes(java_dest: str, exclude: list = None):
    """
    Check if code uses an insecure AES mode.

    AES should not be used with ECB or CBC/PKCS5Padding.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    ecb_mode = '/' + CaselessKeyword('ECB')
    cbc_mode = '/' + CaselessKeyword('CBC')
    padding_pkc = '/' + CaselessKeyword('PKCS5Padding')
    padding_all = '/' + Word(alphanums)
    algorithm = '"' + CaselessKeyword('AES') + Optional(
        ((ecb_mode + padding_all) | (cbc_mode + padding_pkc))) + '"'

    grammar = Suppress(Keyword('Cipher') + '.' + Keyword('getInstance')) + \
        nestedExpr()
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the AES algorithm
        lambda tokens: tokens.asList() and any(
            algorithm.matches(tok) for tok in tokens[0]))

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: f'Code uses insecure AES modes',
            CLOSED: f'Code uses secure AES modes',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(
    risk=MEDIUM,
    kind=SAST,
    standards={
        'CWE': '780',
    },
)
def uses_insecure_rsa(java_dest: str, exclude: list = None) -> tuple:
    """
    Check if RSA algorithm uses an insecure padding.

    :param java_dest: Path to a Java source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    :returns: - ``UNKNOWN`` on errors.
        - ``OPEN`` if an **OAEP** padding is not used or **ECB** mode is used.
        - ``CLOSED`` otherwise.

    """
    insecure_modes = '/' + oneOf('ECB', caseless=True)
    any_modes = '/' + Word(alphanums)

    padding = '/' + Word(alphanums + '-')
    padding.addCondition(lambda tokens: 'oaep' not in str(tokens).lower())
    any_padding = '/' + Word(alphanums + '-')

    algorithm = '"' + CaselessKeyword('RSA') + Optional(
        (insecure_modes + any_padding) | (any_modes + padding)) + '"'

    grammar = Suppress(
        Keyword('Cipher') + '.' + Keyword('getInstance')) + nestedExpr()
    grammar.ignore(javaStyleComment)
    grammar.addCondition(
        # Ensure that at least one token is the RSA algorithm
        lambda tokens: tokens.asList() and any(
            algorithm.matches(tok) for tok in tokens[0]))

    return lang.generic_method(
        path=java_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: (f'Code uses an insecure RSA padding we '
                   'recommend use a OAEP padding'),
            CLOSED:
            f'Code uses a secure RSA padding',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)
