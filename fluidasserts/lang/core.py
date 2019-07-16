# -*- coding: utf-8 -*-

"""This module allows to check generic Code vulnerabilities."""

# standard imports
import re
import os
from base64 import b64encode

# 3rd party imports
from pyparsing import MatchFirst, QuotedString

# local imports
from fluidasserts import Vuln, Result, OPEN, CLOSED, UNKNOWN, LOW
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.decorators import track, level, notify, api


LANGUAGE_SPECS = {}  # type: dict


@track
@api(risk=LOW)
def has_text(code_dest: str, expected_text: str, use_regex: bool = False,
             exclude: list = None, lang_specs: dict = None) -> Result:
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
    """
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    grammar = expected_text if use_regex else re.escape(expected_text)
    matches = lang.check_grammar_re(grammar, code_dest, lang_specs, exclude)

    if not matches:
        return CLOSED, 'Bad text not present in code'

    parsed_matches = [
        Vuln(path, 'lines', data['lines'].split(', '), data['sha256'])
        for path, data in matches.items()]

    return OPEN, 'Bad text present in code', parsed_matches


@notify
@level('low')
@track
def has_not_text(code_dest: str, expected_text: str, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> bool:
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
    """
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    grammar = expected_text if use_regex else re.escape(expected_text)
    try:
        matches = lang.check_grammar_re(grammar, code_dest,
                                        lang_specs, exclude)
        if not matches:
            show_open('Expected text not present in code',
                      details=dict(location=code_dest,
                                   expected_text=expected_text,
                                   used_regular_expressions=use_regex))
            return True
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=code_dest))
        return False
    show_close('Expected text present in code',
               details=dict(matches=matches,
                            expected_text=expected_text,
                            used_regular_expressions=use_regex))
    return False


@notify
@level('low')
@track
def has_all_text(code_dest: str, expected_list: list, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> bool:
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
    """
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    matches = {}
    for expected in set(expected_list):
        grammar = expected if use_regex else re.escape(expected)
        try:
            __matches = lang.check_grammar_re(grammar, code_dest,
                                              lang_specs, exclude)
            if not __matches:
                show_close('Not all expected text was found in code',
                           details=dict(location=code_dest,
                                        expected_list=expected_list,
                                        used_regular_expressions=use_regex))
                return False
            matches.update(__matches)
        except FileNotFoundError:
            show_unknown('File does not exist',
                         details=dict(code_dest=code_dest,
                                      used_regular_expressions=use_regex))
            return False
    show_open('A bad text from list was found in code',
              details=dict(matches=matches,
                           expected_list=expected_list,
                           used_regular_expressions=use_regex))
    return True


@notify
@level('low')
@track
def has_any_text(code_dest: str, expected_list: list, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> bool:
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
    """
    # Remove duplicates
    expected_set = set(expected_list)
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    if not use_regex:
        expected_set = map(re.escape, expected_set)
    any_list = '|'.join(f'(?:{exp})' for exp in expected_set)
    try:
        matches = lang.check_grammar_re(any_list, code_dest,
                                        lang_specs, exclude)
        if not matches:
            show_close('None of the expected strings were found in code',
                       details=dict(location=code_dest,
                                    expected_list=expected_list,
                                    used_regular_expressions=use_regex))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=code_dest))
        return False
    show_open('Any of the expected bad text is present in code',
              details=dict(matches=matches,
                           expected_list=expected_list,
                           used_regular_expressions=use_regex))
    return True


@notify
@level('low')
@track
def has_not_any_text(code_dest: str,
                     expected_list: list, use_regex: bool = False,
                     exclude: list = None, lang_specs: dict = None) -> bool:
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
    """
    # Remove duplicates
    expected_set = set(expected_list)
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    if not use_regex:
        expected_set = map(re.escape, expected_set)
    any_list = '|'.join(f'(?:{exp})' for exp in expected_set)
    try:
        matches = lang.check_grammar_re(any_list, code_dest,
                                        lang_specs, exclude)
        if not matches:
            show_open('None of the expected texts were found in code',
                      details=dict(location=code_dest,
                                   expected_list=expected_list,
                                   used_regular_expressions=use_regex))
            return True
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=code_dest))
        return False
    show_close('Any of the expected texts are present in code',
               details=dict(matches=matches,
                            expected_list=expected_list,
                            used_regular_expressions=use_regex))
    return False


@notify
@level('low')
@track
def file_exists(code_file: str) -> bool:
    """
    Check if the given file exists.

    :param code_file: Path to the file to be tested.
    """
    if os.path.exists(code_file):
        show_open('File exists',
                  details=dict(path=code_file,
                               fingerprint=get_sha256(code_file)))
        return True
    show_close('File does not exist',
               details=dict(path=code_file,
                            fingerprint=get_sha256(code_file)))
    return False


@notify
@level('low')
@track
def file_does_not_exist(code_file: str) -> bool:
    """
    Check if the given file does'nt exist.

    :param code_file: Path to the file to be tested.
    """
    if os.path.exists(code_file):
        show_close('File exists',
                   details=dict(path=code_file,
                                fingerprint=get_sha256(code_file)))
        return False
    show_open('File does not exist',
              details=dict(path=code_file,
                           fingerprint=get_sha256(code_file)))
    return True


@notify
@level('medium')
@track
def has_weak_cipher(code_dest: str, expected_text: str,
                    exclude: list = None, lang_specs: dict = None) -> bool:
    """
    Check if code uses base 64 to cipher confidential data.

    See `REQ.185 <https://fluidattacks.com/web/rules/185/>`_.

    :param code_dest: Path to a code source file or package.
    :param expected_text: Text that might be in source file or package
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    """
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    grammar = re.escape(b64encode(expected_text.encode()).decode())
    try:
        b64_matches = lang.check_grammar_re(grammar, code_dest,
                                            lang_specs, exclude)
        if not b64_matches:
            show_close(
                'Code does not have confidential data encoded in base64',
                details=dict(location=code_dest))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(code_dest=code_dest))
        return False
    else:
        for code_file, vulns in b64_matches.items():
            show_open('Code has confidential data encoded in base64',
                      details=dict(expected=expected_text,
                                   file=code_file,
                                   fingerprint=lang.
                                   get_sha256(code_file),
                                   lines=str(vulns)[1:-1],
                                   total_vulns=len(vulns)))
    return True


@notify
@level('high')
@track
def has_secret(code_dest: str, secret: str, use_regex: bool = False,
               exclude: list = None, lang_specs: dict = None) -> bool:
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
    """
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    grammar = secret if use_regex else re.escape(secret)
    try:
        matches = lang.check_grammar_re(grammar, code_dest,
                                        lang_specs, exclude)
        if not matches:
            show_close('Secret not found in code',
                       details=dict(location=code_dest,
                                    secret=secret,
                                    used_regular_expressions=use_regex))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(location=code_dest))
        return False
    show_open('Secret found in code',
              details=dict(matches=matches,
                           secret=secret,
                           used_regular_expressions=use_regex))
    return True


@notify
@level('high')
@track
def has_any_secret(code_dest: str, secrets_list: list, use_regex: bool = False,
                   exclude: list = None, lang_specs: dict = None) -> bool:
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
    """
    # Remove duplicates
    secrets_set = set(secrets_list)
    if not lang_specs:
        lang_specs = LANGUAGE_SPECS
    if not use_regex:
        secrets_set = map(re.escape, secrets_set)
    any_list = '|'.join(f'(?:{exp})' for exp in secrets_set)
    try:
        matches = lang.check_grammar_re(any_list, code_dest,
                                        lang_specs, exclude)
        if not matches:
            show_close('None of the expected secrets were found in code',
                       details=dict(location=code_dest,
                                    secrets_list=secrets_list,
                                    used_regular_expressions=use_regex))
            return False
    except FileNotFoundError:
        show_unknown('File does not exist',
                     details=dict(code_dest=code_dest))
        return False
    show_open('Some of the expected secrets are present in code',
              details=dict(matches=matches,
                           secrets_list=secrets_list,
                           used_regular_expressions=use_regex))
    return True


@notify
@level('medium')
@track
def uses_unencrypted_sockets(
        code_dest: str, exclude: list = None, lang_specs: dict = None) -> bool:
    """
    Check if there are unencrypted web sockets URI schemes in code (`ws://`).

    :param code_dest: Path to the file or directory to be tested.
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
    """
    encrypted_re = re.compile(r'^wss://.*$', flags=re.I)
    unencrypted_re = re.compile(r'^ws://.*$', flags=re.I)

    encrypted_grammar = MatchFirst([QuotedString('"'), QuotedString("'")])
    unencrypted_grammar = MatchFirst([QuotedString('"'), QuotedString("'")])

    encrypted_grammar.addCondition(lambda x: encrypted_re.search(x[0]))
    unencrypted_grammar.addCondition(lambda x: unencrypted_re.search(x[0]))

    try:
        unencrypted = lang.path_contains_grammar(
            unencrypted_grammar, code_dest, LANGUAGE_SPECS, exclude)
    except FileNotFoundError:
        show_unknown('File does not exist', details=dict(code_dest=code_dest))
        return False

    if unencrypted:
        show_open('Code uses web sockets over an unencrypted channel',
                  details=dict(vulnerable_uris=unencrypted))
        return True

    encrypted = lang.path_contains_grammar(
        encrypted_grammar, code_dest, LANGUAGE_SPECS, exclude)

    if encrypted:
        msg = 'Code uses web sockets over an encrypted channel'
    else:
        msg = 'Cose does not use web sockets'
    show_close(msg, details=dict(code_dest=code_dest, checked_uris=encrypted))
    return False
