# -*- coding: utf-8 -*-

"""This module allows to check generic Code vulnerabilities."""

# standard imports
import re
import os
from base64 import b64encode
from typing import List

# 3rd party imports
from pyparsing import (cppStyleComment, Char, Keyword, Literal, MatchFirst,
                       nestedExpr, Optional, QuotedString, Regex, ZeroOrMore,
                       Suppress, ParserElement)

# local imports
from fluidasserts import Unit, LOW, MEDIUM, HIGH, OPEN, CLOSED, UNKNOWN, SAST
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256, get_paths
from fluidasserts.utils.decorators import api

# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')


def _flatten(elements, aux_list=None):
    aux_list = aux_list if aux_list is not None else []
    for i in elements:
        if isinstance(i, (list, tuple)):
            _flatten(i, aux_list)
        else:
            aux_list.append(i)
    return aux_list


def generic_c_has_if_without_else(
        location: str,
        conditions: list,
        use_regex: bool = False,
        lang_specs: dict = None,
        exclude: list = None) -> tuple:
    """Perform a generic has_if_without_else that can be reused."""
    no_else_found = '__no_else_found__'

    content = MatchFirst([
        Regex(condition) if use_regex else Literal(condition)
        for condition in conditions])

    args_if = '(' + content + ')'
    args_else_if = nestedExpr(opener='(', closer=')')
    block = nestedExpr(opener='{', closer='}')

    if_block = Keyword('if') + args_if + block
    else_if_block = Keyword('else') + Keyword('if') + args_else_if + block
    else_block = Optional(Keyword('else') + block, default=no_else_found)

    else_block.addCondition(lambda x: no_else_found in str(x))

    grammar = if_block + ZeroOrMore(else_if_block) + else_block
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_CHAR)
    grammar.ignore(L_STRING)

    return lang.generic_method(
        path=location,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has "if" without "else" clause',
            CLOSED: 'Code has "if" with "else" clause',
        },
        spec=lang_specs,
        excl=exclude)


def _switch_condition(tokens):
    default = Literal('default') + Char(':')
    result = []
    for item in tokens:
        iters = _flatten(item)
        for index, value in enumerate(iters):
            if value == 'default' and iters[index + 1] == ':':
                result.append(False)
            else:
                result.append(not default.searchString(str(value)))
    return all(result)


def generic_c_has_switch_without_default(
        location: str, lang_specs: dict = None, exclude: list = None) -> tuple:
    r"""
    Check if all ``switch``\ es have a ``default`` clause.

    See `REQ.161 <https://fluidattacks.com/web/rules/161/>`_.

    See `CWE-478 <https://cwe.mitre.org/data/definitions/478.html>`_.

    :param location: Path to a source file or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    switch = Keyword('switch') + nestedExpr(opener='(', closer=')')
    grammar = Suppress(switch) + nestedExpr(opener='{', closer='}')
    grammar.ignore(cppStyleComment)
    grammar.ignore(L_STRING)
    grammar.ignore(L_CHAR)
    grammar.addCondition(_switch_condition)

    return lang.generic_method(
        path=location,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code does not have "switch" with "default" clause',
            CLOSED: 'Code has "switch" with "default" clause',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_text(code_dest: str,
             expected_text: str,
             open_message: str,
             closed_message: str,
             use_regex: bool =
             False,
             exclude: list = None,
             lang_specs: dict = None) -> tuple:
    """
    Check if a bad text is present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param expected_text: Bad text to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(expected_text) if use_regex else Literal(expected_text)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: open_message,
            CLOSED: closed_message,
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_not_text(code_dest: str, expected_text: str, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if a required text is not present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param expected_text: Bad text to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(expected_text) if use_regex else Literal(expected_text)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Expected text not present in code',
            CLOSED: 'Expected text present in code',
        },
        spec=lang_specs,
        excl=exclude,
        reverse=True)


@api(risk=LOW, kind=SAST)
def has_all_text(code_dest: str, expected_list: list, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if a list of bad text is present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param expected_list: List of bad text to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    vulns, safes = [], []

    lang_specs = lang_specs if lang_specs else {}

    for expected in set(expected_list):
        grammar = Regex(expected) if use_regex else Literal(expected)

        _vulns, _safes = lang.parse(grammar, code_dest, lang_specs, exclude)

        if not _vulns:
            return CLOSED, 'Not all expected text was found in code'
        vulns.extend(_vulns)
        safes.extend(_safes)

    if vulns:
        return OPEN, 'All text from list was found in code', vulns, safes
    return CLOSED, 'No files were tested', vulns, safes


@api(risk=LOW, kind=SAST)
def has_any_text(code_dest: str, expected_list: list, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if any on a list of bad text is present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param expected_list: List of bad text to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(expected_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(expected_list)])

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'An expected text is present in code',
            CLOSED: 'No expected text was found in code',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_not_any_text(code_dest: str,
                     expected_list: list, use_regex: bool = False,
                     exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if not any on a list of bad text is present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param expected_list: List of bad text to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(expected_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(expected_list)])

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Expected text is not present in code',
            CLOSED: 'Expected text is present in code',
        },
        spec=lang_specs,
        excl=exclude,
        reverse=True)


@api(risk=LOW, kind=SAST)
def file_exists(code_file: str) -> tuple:
    """
    Check if the given file exists.

    :param code_file: Path to the file to be tested.
    :rtype: :class:`fluidasserts.Result`
    """
    if os.path.exists(code_file):
        vulns = [Unit(where=code_file,
                      source='File',
                      specific=['Exists'],
                      fingerprint=get_sha256(code_file))]
        return OPEN, 'File exists', vulns
    return CLOSED, 'File does not exist'


@api(risk=LOW, kind=SAST)
def file_does_not_exist(code_file: str) -> tuple:
    """
    Check if the given file doesn't exist.

    :param code_file: Path to the file to be tested.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(code_file):
        vulns = [Unit(where=code_file,
                      source='File',
                      specific=['Does not exist'],
                      fingerprint=get_sha256(code_file))]
        return OPEN, 'File does not exists', vulns
    return CLOSED, 'File exist'


@api(risk=MEDIUM, kind=SAST)
def is_file_hash_in_list(path: str, hash_list: List[str]) -> tuple:
    """
    Check if the given file hash is in a list of given hashes.

    :param path: Path to the file to be tested.
    :param hash_list: List of expected hashes.
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(path):
        return UNKNOWN, 'File does not exists'
    vulns, safes = [], []
    for full_path in get_paths(path):
        fingerprint: str = get_sha256(full_path)
        if fingerprint in hash_list:
            vulns.append(Unit(where=full_path,
                              source='File',
                              specific=['Matches hash'],
                              fingerprint=fingerprint))
        else:
            safes.append(Unit(where=full_path,
                              source='File',
                              specific=['Does not match hash'],
                              fingerprint=fingerprint))

    if vulns:
        msg = 'Path contain files whose hash is in given list'
        return OPEN, msg, vulns, safes
    msg = 'Path does not contain files whose hash is in given list'
    return CLOSED, msg, vulns, safes


@api(risk=MEDIUM, kind=SAST)
def has_weak_cipher(code_dest: str, expected_text: str,
                    exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if code uses base 64 to cipher confidential data.

    See `REQ.185 <https://fluidattacks.com/web/rules/185/>`_.

    :param code_dest: Path to a code source file or package.
    :param expected_text: Text that might be in source file or package
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Literal(b64encode(expected_text.encode()).decode())
    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code has confidential data encoded in base64',
            CLOSED: 'Code does not have confidential data encoded in base64',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=HIGH, kind=SAST)
def has_secret(code_dest: str, secret: str, use_regex: bool = False,
               exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if a secret is present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param secret: Secret to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(secret) if use_regex else Literal(secret)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Secret found in code',
            CLOSED: 'Secret not found in code',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=HIGH, kind=SAST)
def has_any_secret(code_dest: str, secrets_list: list, use_regex: bool = False,
                   exclude: list = None, lang_specs: dict = None) -> tuple:
    """
    Check if any on a list of secrets is present in given source file.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param secrets_list: List of secrets to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(secrets_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(secrets_list)])

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Some of the expected secrets are present in code',
            CLOSED: 'None of the expected secrets were found in code',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=MEDIUM, kind=SAST)
def uses_unencrypted_sockets(code_dest: str,
                             exclude: list = None,
                             lang_specs: dict = None) -> tuple:
    """
    Check if there are unencrypted web sockets URI schemes in code (`ws://`).

    :param code_dest: Path to the file or directory to be tested.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    unencrypted_re = re.compile(r'^ws://.*$', flags=re.I)
    grammar = MatchFirst([QuotedString('"'), QuotedString("'")])
    grammar.addCondition(lambda x: unencrypted_re.search(x[0]))

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code uses web sockets over an encrypted channel',
            CLOSED: 'Code does not use web sockets over an encrypted channel',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_unnecessary_permissions(code_dest: str,
                                permission: str,
                                use_regex: bool = False,
                                exclude: list = None,
                                lang_specs: dict = None) -> tuple:
    """
    Check if the application has unnecessary permissions.

    Granting unnecessary permissions to the application could allow the
    attacker to escalate privileges through the permissions that have been
    granted to the application.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param permission: permission format to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(permission) if use_regex else Literal(permission)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Permmission found in the code.',
            CLOSED: 'Permission not found in the code.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW,
     kind=SAST,
     standards={
         'CWE': '396',
     },)
def has_generic_exceptions(code_dest: str,
                           exception: str,
                           use_regex: bool = False,
                           exclude: list = None,
                           lang_specs: dict = None) -> tuple:
    """
    Check if a generic exception is present in given source file.

    The software does not properly anticipate or handle exceptional conditions
    that rarely occur during normal operation of the software.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param secret: Generic Exception format to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(exception) if use_regex else Literal(exception)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Generic exception found in the code.',
            CLOSED: 'Generic exception not found in the code.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def leaks_technical_information(code_dest: str,
                                pattern: str,
                                use_regex: bool = False,
                                exclude: list = None,
                                lang_specs: dict = None):
    """
    Check if there are code that leaks technical information.

    The leak of technical information can inform the attacker of sensitive
    information about the environment where the application is executed and
    reveal a possible attack surface.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param pattern: Text pattern to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(pattern) if use_regex else Literal(pattern)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: ('Text pattern that generates leakage of'
                   ' technical information found in the code.'),
            CLOSED: ('No text patterns that generate leaks of technical'
                     ' information were found in code'),
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_insecure_settings(code_dest: str,
                          settting: str,
                          use_regex: bool = False,
                          exclude: list = None,
                          lang_specs: dict = None):
    """
    Check if the code has services with insecure settings.

    Unsafe settings of a service can open several security breaches that
    could affect the service.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param setting: Setting to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(settting) if use_regex else Literal(settting)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Insecure settings found in the code.',
            CLOSED: 'Insecure settings not found in the code.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_code_injection(code_dest: str,
                       pattern: str,
                       use_regex: bool = False,
                       exclude: list = None,
                       lang_specs: dict = None):
    """
    Check if the code has patterns that generate code injections.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param setting: Pattern to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(pattern) if use_regex else Literal(pattern)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Pattern found in code.',
            CLOSED: 'Pattern not found in code.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_vulnerable_dependencies(code_dest: str,
                                dependence: str,
                                use_regex: bool = False,
                                exclude: list = None,
                                lang_specs: dict = None):
    """
    Check if there are vulnerable dependencies.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param dependency: Dependence to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(dependence) if use_regex else Literal(dependence)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Vulnerable dependencies are present.',
            CLOSED: 'There are no vulnerable dependencies.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def use_insecure_methods(code_dest: str,
                         method: str,
                         use_regex: bool = False,
                         exclude: list = None,
                         lang_specs: dict = None):
    """
    Check if the code uses insecure methods.

    The use of insecure methods can generate security breaches that can be
    exploited by attackers who are aware of the vulnerabilities of the methods.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param method: Method to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(method) if use_regex else Literal(method)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Insecure methods are present.',
            CLOSED: 'There are no insecure methods present.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def missing_input_data_validation(code_dest: str,
                                  pattern: str,
                                  use_regex: bool = False,
                                  exclude: list = None,
                                  lang_specs: dict = None):
    """
    Check if the code does not validate the input data.

    An attacker can take advantage of the lack of server-side data validation
    to create an injection (XSS, SQLi, HTML) to expand the attack surface.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param pattern: Pattern to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(pattern) if use_regex else Literal(pattern)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Missing validation of the input data.',
            CLOSED: 'Validation of the input data is done.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_log_injection(code_dest: str,
                      pattern: str,
                      use_regex: bool = False,
                      exclude: list = None,
                      lang_specs: dict = None):
    """
    Check if the code allow log injection.

    Writing unvalidated user input to log files can allow an attacker to forge
    log entries or inject malicious content into the logs.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param information: Information to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(pattern) if use_regex else Literal(pattern)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'The code allows log injection.',
            CLOSED: 'The code does not allow log injection.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def exposes_sensitive_information(code_dest: str,
                                  pattern: str,
                                  use_regex: bool = False,
                                  exclude: list = None,
                                  lang_specs: dict = None):
    """
    Check if the code exposes sensitive information.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param information: Information to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(pattern) if use_regex else Literal(pattern)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'The code expose sensitive information.',
            CLOSED: 'The code does not expose sensitive information.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def uses_insecure_protocol(code_dest: str,
                           pattern: str,
                           use_regex: bool = False,
                           exclude: list = None,
                           lang_specs: dict = None):
    """
    Check if the code uses insecure protocol.

    The information transits through a non-encrypted channel, the information
    can be captured in plain text.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param pattern: Pattern to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    grammar = Regex(pattern) if use_regex else Literal(pattern)

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'The code uses insecure protocol.',
            CLOSED: 'The code does not use insecure protocols.',
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_grammar(code_dest: str,
                grammar: ParserElement,
                open_message: str,
                closed_message: str,
                exclude: list = None,
                lang_specs: dict = None) -> tuple:
    """
    Check if a grammar is present in given source file.

    :param code_dest: Path to the file or directory to be tested.
    :param grammar: Grammar to be searched for in path.
    :open_message: Message to show for open vulnerabilities.
    :closed_message: Message to show for closed vulnerabilities.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: open_message,
            CLOSED: closed_message,
        },
        spec=lang_specs,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_sensible_data_in_logs(code_dest: str,
                              expected_list: list,
                              use_regex: bool = False,
                              exclude: list = None,
                              lang_specs: dict = None) -> tuple:
    """
    Check if the code stores critical system or user data in the logs.

    if `use_regex` equals True, Search is (case-insensitively)
    performed by :py:func:`re.search`.

    :param code_dest: Path to the file or directory to be tested.
    :param expected_list: List of bad text to look for in the file.
    :param use_regex: Use regular expressions instead of literals to search.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    :rtype: :class:`fluidasserts.Result`
    """
    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(expected_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(expected_list)])

    return lang.generic_method(
        path=code_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'There is sensitive data being stored in logs',
            CLOSED: 'There is no sensitive data being stored in logs',
        },
        spec=lang_specs,
        excl=exclude)
