# -*- coding: utf-8 -*-

"""This module allows to check vulnerabilities in Dockerfiles."""

# standard imports
import os
from typing import Dict, Any

# 3rd party imports
from pyparsing import Regex, Keyword, Optional, Combine, ZeroOrMore

# local imports
from fluidasserts import Result
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts import LOW
from fluidasserts import SAST
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api


LANGUAGE_SPECS: Dict[str, Any] = {
    'extensions': None,
    'block_comment_start': None,
    'block_comment_end': None,
    'line_comment': ('#',),
}


# Following regex were taken from Docker source code:
#   https://github.com/docker/distribution/blob/master/reference/regexp.go

D_TAG = Regex(r'[\w][\w.-]{0,127}')

ALPHANUM = Regex(r'[a-zA-Z0-9]+')
SEPARATOR = Regex(r'(?:[._]|__|[-]*)')

_DOMAIN = Regex(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*))')
D_DOMAIN = \
    _DOMAIN + ZeroOrMore('.' + _DOMAIN) + Optional(':' + Regex(r'[0-9]+'))

_NAME = ALPHANUM + ZeroOrMore(SEPARATOR + ALPHANUM)
D_NAME = Combine(Optional(D_DOMAIN + '/') + _NAME + ZeroOrMore('/' + _NAME))


@api(risk=LOW, kind=SAST)
def not_pinned(file_dest: str, exclude: list = None) -> Result:
    """
    Check if the Dockerfile uses a ``FROM:...latest`` (unpinned) base image.

    :param file_dest: Path to the Dockerfile to be tested.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: True if unpinned (bad), False if pinned (good).
    """
    if not os.path.exists(file_dest):
        return UNKNOWN, 'File does not exist'

    pinned = Keyword('FROM') + D_NAME + Optional(':' + D_TAG)
    pinned.setDefaultWhitespaceChars(' \t\r')
    pinned.addCondition(
        # x = ['FROM', 'D_NAME', ':', 'D_TAG']
        lambda x: len(x) == 2 or (len(x) == 4 and x[3] == 'latest'))

    vulns, safes = \
        lang.check_grammar2(pinned, file_dest, LANGUAGE_SPECS, exclude)

    if vulns:
        return OPEN, 'Dockerfile uses unpinned base image(s)', vulns
    if safes:
        return CLOSED, 'Dockerfile has pinned base image(s)', vulns, safes

    return CLOSED, 'No files were tested'
