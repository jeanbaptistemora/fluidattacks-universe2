# -*- coding: utf-8 -*-

"""This module allows to check generic Code vulnerabilities."""

# standard imports
import re
import os
from base64 import b64encode

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
    if not os.path.exists(code_dest):
        return UNKNOWN, 'File does not exist'

    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    grammar = Regex(expected_text) if use_regex else Literal(expected_text)
    vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'Bad text present in code', vulns
    return CLOSED, 'Bad text not present in code'


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

    open_vulns = lang.check_grammar2(
        grammar, code_dest, lang_specs, exclude, positive_search=False)

    if open_vulns:
        return OPEN, 'Expected text not present in code', open_vulns

    closed_vulns = lang.check_grammar2(
        grammar, code_dest, lang_specs, exclude)

    if closed_vulns:
        closed_vulns = [Safe(where=x.where,
                             attribute=x.attribute,
                             specific=x.specific,
                             fingerprint=x.fingerprint) for x in closed_vulns]
        return \
            CLOSED, 'Expected text present in code', open_vulns, closed_vulns

    return OPEN, 'No files has been processed, therefore there is no text'


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

    vulns = []
    lang_specs = LANGUAGE_SPECS if not lang_specs else lang_specs

    for expected in set(expected_list):
        grammar = Regex(expected) if use_regex else Literal(expected)

        __vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

        if not __vulns:
            return CLOSED, 'Not all expected text was found in code'
        vulns.extend(__vulns)

    return OPEN, 'A bad text from list was found in code', vulns


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

    vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'Any of the expected bad text is present in code', vulns
    return CLOSED, 'None of the expected strings were found in code'


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

    vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return CLOSED, 'Any of the expected texts are present in code'
    return OPEN, 'None of the expected texts were found in code', vulns


@notify
@api(risk=LOW)
def file_exists(code_file: str) -> Result:
    """
    Check if the given file exists.

    :param code_file: Path to the file to be tested.
    """
    if os.path.exists(code_file):
        vulns = [Vuln(where=code_file,
                      attribute='lines',
                      specific=[0],
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
                      attribute='lines',
                      specific=[0],
                      fingerprint=get_sha256(code_file))]
        return OPEN, 'File does not exists', vulns
    return CLOSED, 'File exist'


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
    vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'Code has confidential data encoded in base64', vulns
    return CLOSED, 'Code does not have confidential data encoded in base64'


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

    vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)
    if vulns:
        return OPEN, 'Secret found in code', vulns
    return CLOSED, 'Secret not found in code'


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

    vulns = lang.check_grammar2(grammar, code_dest, lang_specs, exclude)

    if vulns:
        return OPEN, 'Some of the expected secrets are present in code', vulns
    return CLOSED, 'None of the expected secrets were found in code'


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
