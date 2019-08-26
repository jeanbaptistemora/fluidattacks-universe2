# -*- coding: utf-8 -*-

"""This module allows to check generic Code vulnerabilities."""

# standard imports
import re
import os
from base64 import b64encode
from typing import List

# 3rd party imports
from pyparsing import (cppStyleComment, Keyword, Literal, MatchFirst,
                       nestedExpr, Optional, QuotedString, Regex, ZeroOrMore)

# local imports
from fluidasserts import Unit, LOW, MEDIUM, HIGH, OPEN, CLOSED, UNKNOWN, SAST
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256, get_paths
from fluidasserts.utils.decorators import api

# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')

LANGUAGE_SPECS = {}  # type: dict


def _generic_c_has_if_without_else(
        location: str,
        conditions: list,
        use_regex: bool = False,
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
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code has "if" without "else" clause',
            CLOSED: 'Code has "if" with "else" clause',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)


@api(risk=LOW, kind=SAST)
def has_text(code_dest: str, expected_text: str, use_regex: bool = False,
             exclude: list = None, lang_specs: dict = None) -> tuple:
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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    grammar = Regex(expected_text) if use_regex else Literal(expected_text)
    vulns, safes = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'Text is present in code', vulns, safes
    if safes:
        return CLOSED, 'Bad text not present in code', vulns, safes

    return CLOSED, 'No files were tested', vulns, safes


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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    grammar = Regex(expected_text) if use_regex else Literal(expected_text)

    safes, vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'Expected text not present in code', vulns, safes
    if safes:
        return CLOSED, 'Expected text present in code', vulns, safes

    return OPEN, 'No files were tested', vulns, safes


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
    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    for expected in set(expected_list):
        grammar = Regex(expected) if use_regex else Literal(expected)

        _vulns, _safes = \
            lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(expected_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(expected_list)])

    vulns, safes = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'An expected text is present in code', vulns, safes
    return CLOSED, 'No expected text was found in code', vulns, safes


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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(expected_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(expected_list)])

    vulns, safes = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return CLOSED, 'Expected text is present in code', vulns, safes
    return OPEN, 'No expected text was found in code', vulns, safes


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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    grammar = Literal(b64encode(expected_text.encode()).decode())
    vulns, safes = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        msg = 'Code has confidential data encoded in base64'
        return OPEN, msg, vulns, safes
    msg = 'No files were tested'
    if safes:
        msg = 'Code does not have confidential data encoded in base64'
    return CLOSED, msg, vulns, safes


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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    grammar = Regex(secret) if use_regex else Literal(secret)

    vulns, safes = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)
    if vulns:
        return OPEN, 'Secret found in code', vulns, safes
    if safes:
        return CLOSED, 'Secret not found in code', vulns, safes
    return CLOSED, 'No files were tested'


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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    if use_regex:
        grammar = MatchFirst([Regex(x) for x in set(secrets_list)])
    else:
        grammar = MatchFirst([Literal(x) for x in set(secrets_list)])

    vulns, safes = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        msg = 'Some of the expected secrets are present in code'
        return OPEN, msg, vulns
    msg = 'No files were tested'
    if safes:
        msg = 'None of the expected secrets were found in code'
    return CLOSED, msg, vulns, safes


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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    unencrypted_re = re.compile(r'^ws://.*$', flags=re.I)
    unencrypted_grammar = MatchFirst([QuotedString('"'), QuotedString("'")])
    unencrypted_grammar.addCondition(lambda x: unencrypted_re.search(x[0]))

    return lang.generic_method(
        path=code_dest,
        gmmr=unencrypted_grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code uses web sockets over an encrypted channel',
            CLOSED: 'Code does not use web sockets over an encrypted channel',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)
