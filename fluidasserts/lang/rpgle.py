# -*- coding: utf-8 -*-

"""This module allows to check RPGLE code vulnerabilities."""

# standard imports
import os
from typing import Dict, Any

# 3rd party imports
from pyparsing import (CaselessKeyword, Keyword, Word, Optional,
                       NotAny, alphas, alphanums, nums, cppStyleComment,
                       MatchFirst, delimitedList)

# local imports
from fluidasserts import Result
from fluidasserts import LOW, MEDIUM
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts import SAST
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api

LANGUAGE_SPECS: Dict[str, Any] = {
    'extensions': ('rpg', 'rpgle',),
    'block_comment_start': None,
    'block_comment_end': None,
    'line_comment': ('//', '*',),
}

VAR_NAME = Word(alphas + "_", alphanums + "_")
ON_ERROR = CaselessKeyword('on-error')
ERROR_CODE = MatchFirst([
    Word(nums),
    CaselessKeyword('*PROGRAM'),
    CaselessKeyword('*FILE'),
    CaselessKeyword('*ALL'),
])
ERROR_CODES = delimitedList(ERROR_CODE, delim=':')


@api(risk=MEDIUM, kind=SAST)
def has_dos_dow_sqlcod(rpg_dest: str, exclude: list = None) -> Result:
    r"""
    Search for DoS for using ``DoW SQLCOD = <ZERO>``\ .

    :param rpg_dest: Path to a RPG source or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    if not os.path.exists(rpg_dest):
        return UNKNOWN, 'File does not exist'

    tk_dow = CaselessKeyword('dow')
    tk_sqlcod = CaselessKeyword('sqlcod')
    tk_literal_zero = CaselessKeyword('*zeros')

    grammar = tk_dow + tk_sqlcod + '=' + ('0' | tk_literal_zero)

    vulns, safes = \
        lang.check_grammar2(grammar, rpg_dest, LANGUAGE_SPECS, exclude)

    if vulns:
        msg = 'Code does have DoS for using "DoW SQLCOD = 0"'
        return OPEN, msg, vulns, safes
    if safes:
        msg = 'Code does not have DoS for using "DoW SQLCOD = 0"'
        return CLOSED, msg, vulns, safes
    return CLOSED, 'No files were tested'


@api(risk=LOW, kind=SAST)
def has_unitialized_vars(rpg_dest: str, exclude: list = None) -> Result:
    """
    Search for unitialized variables.

    :param rpg_dest: Path to a RPG source or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    if not os.path.exists(rpg_dest):
        return UNKNOWN, 'File does not exist'

    tk_data = Keyword('D')
    tk_vartype = Word(alphas, exact=1)
    tk_varlen = Word(nums) + Word(alphas, exact=1)
    tk_inz = CaselessKeyword('inz')

    grammar = tk_data + VAR_NAME + Optional(tk_vartype) + \
        Optional(tk_varlen) + Optional(Word(nums)) + NotAny(tk_inz)

    vulns, safes = \
        lang.check_grammar2(grammar, rpg_dest, LANGUAGE_SPECS, exclude)

    if vulns:
        return OPEN, 'Code has unitialized variables', vulns, safes
    if safes:
        return CLOSED, 'Code does not have unitialized variables', vulns, safes
    return CLOSED, 'No files were tested'


@api(risk=LOW, kind=SAST)
def has_generic_exceptions(rpg_dest: str, exclude: list = None) -> Result:
    """
    Search for on-error empty or *PROGRAM, *FILE, or *ALL codes.

    See `REQ. 161
    <https://fluidattacks.com/web/rules/161/>`_.

    :param rpg_dest: Path to a RPG source or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    if not os.path.exists(rpg_dest):
        return UNKNOWN, 'File does not exist'

    generics_list = ('*PROGRAM', '*FILE', '*ALL')

    generics = ERROR_CODES.copy()
    generics.addCondition(
        lambda t: not t or any(x.upper() in generics_list for x in t))

    grammar = ON_ERROR + generics

    vulns, safes = \
        lang.path_contains_grammar2(grammar, rpg_dest, LANGUAGE_SPECS, exclude)

    if vulns:
        return OPEN, 'Code has generic/empty monitors', vulns, safes
    if safes:
        return CLOSED, \
            'Code does not have generic/empty monitors', vulns, safes
    return CLOSED, 'No files were tested'


@api(risk=LOW, kind=SAST)
def swallows_exceptions(rpg_dest: str, exclude: list = None) -> Result:
    """
    Search for on-error without code.

    See `REQ.075 <https://fluidattacks.com/web/rules/075>`_.

    :param rpg_dest: Path to a RPG source or directory.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    if not os.path.exists(rpg_dest):
        return UNKNOWN, 'File does not exist'

    monitor = ON_ERROR + Optional(ERROR_CODES) + Optional(';')
    end_monitor = CaselessKeyword('endmon') + Optional(';')
    grammar = MatchFirst([
        monitor + end_monitor,
        monitor + monitor])
    grammar.ignore(cppStyleComment)

    vulns, safes = lang.path_contains_grammar2(grammar, rpg_dest,
                                               LANGUAGE_SPECS, exclude)

    if vulns:
        return OPEN, 'Code swallows exceptions', vulns, safes
    if safes:
        return CLOSED, 'Code does not swallow exceptions', vulns, safes

    return CLOSED, 'No files were tested'
