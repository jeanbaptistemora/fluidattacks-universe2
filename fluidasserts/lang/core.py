# -*- coding: utf-8 -*-

"""This module allows to check generic Code vulnerabilities."""

# standard imports
import re
import os
from base64 import b64encode
from typing import List

# 3rd party imports
from pyparsing import MatchFirst, QuotedString, Regex, Literal

# local imports
from fluidasserts import Result, Vuln, Safe
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts import LOW, MEDIUM, HIGH
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import lang
from fluidasserts.utils.generic import get_sha256, full_paths_in_dir
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


@track
@api(risk=LOW)
def has_not_text(code_dest: str, expected_text: str, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> Result:
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


@notify
@api(risk=LOW)
def has_all_text(code_dest: str, expected_list: list, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> Result:
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


@notify
@api(risk=LOW)
def has_any_text(code_dest: str, expected_list: list, use_regex: bool = False,
                 exclude: list = None, lang_specs: dict = None) -> Result:
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


@notify
@api(risk=LOW)
def has_not_any_text(code_dest: str,
                     expected_list: list, use_regex: bool = False,
                     exclude: list = None, lang_specs: dict = None) -> Result:
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


@notify
@api(risk=LOW)
def file_exists(code_file: str) -> Result:
    """
    Check if the given file exists.

    :param code_file: Path to the file to be tested.
    """
    if os.path.exists(code_file):
        vulns = [Vuln(where=code_file,
                      fingerprint=get_sha256(code_file))]
        return OPEN, 'File exists', vulns
    return CLOSED, 'File does not exist'


@notify
@api(risk=LOW)
def file_does_not_exist(code_file: str) -> Result:
    """
    Check if the given file does'nt exist.

    :param code_file: Path to the file to be tested.
    """
    if not os.path.exists(code_file):
        vulns = [Vuln(where=code_file,
                      fingerprint=get_sha256(code_file))]
        return OPEN, 'File does not exists', vulns
    return CLOSED, 'File exist'


@notify
@api(risk=MEDIUM)
def is_file_hash_in_list(path: str, hash_list: List[str]) -> Result:
    """
    Check if the given file hash is in a list of given hashes.

    :param path: Path to the file to be tested.
    :param hash_list: List of expected hashes.
    """
    if not os.path.exists(path):
        return UNKNOWN, 'File does not exists'
    vulns, safes = [], []
    for full_path in full_paths_in_dir(path):
        fingerprint: str = get_sha256(full_path)
        if fingerprint in hash_list:
            vulns.append(Vuln(where=full_path,
                              fingerprint=fingerprint))
        else:
            safes.append(Safe(where=full_path,
                              fingerprint=fingerprint))

    if vulns:
        msg = 'Path contain files whose hash is in given list'
        return OPEN, msg, vulns, safes
    msg = 'Path does not contain files whose hash is in given list'
    return CLOSED, msg, vulns, safes


@notify
@api(risk=MEDIUM)
def has_weak_cipher(code_dest: str, expected_text: str,
                    exclude: list = None, lang_specs: dict = None) -> Result:
    """
    Check if code uses base 64 to cipher confidential data.

    See `REQ.185 <https://fluidattacks.com/web/rules/185/>`_.

    :param code_dest: Path to a code source file or package.
    :param expected_text: Text that might be in source file or package
    :param exclude: Paths that contains any string from this list are ignored.
    :param lang_specs: Specifications of the language, see
                       fluidasserts.lang.java.LANGUAGE_SPECS for an example.
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


@notify
@api(risk=HIGH)
def has_secret(code_dest: str, secret: str, use_regex: bool = False,
               exclude: list = None, lang_specs: dict = None) -> Result:
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


@notify
@api(risk=HIGH)
def has_any_secret(code_dest: str, secrets_list: list, use_regex: bool = False,
                   exclude: list = None, lang_specs: dict = None) -> Result:
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
