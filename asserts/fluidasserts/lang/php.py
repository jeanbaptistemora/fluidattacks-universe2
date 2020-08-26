# -*- coding: utf-8 -*-

"""This module allows to check PHP code vulnerabilities."""

# standard imports
# None

# 3rd party imports
from pyparsing import (Keyword, oneOf, Regex, cppStyleComment,
                       pythonStyleComment)

# local imports
from fluidasserts import HIGH, OPEN, CLOSED, SAST
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api


LANGUAGE_SPECS = {
    'extensions': ('php', 'php4', 'php5', 'php6', 'php7',),
    'block_comment_start': '/*',
    'block_comment_end': '*/',
    'line_comment': ('#', '//',)
}  # type: dict


@api(risk=HIGH, kind=SAST)
def has_preg_ce(php_dest: str, exclude: list = None) -> tuple:
    """
    Search for preg_replace calls with '/e'.

    :param php_dest: Path to a PHP script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    quote = oneOf(["'", '"'])
    grammar = Keyword('preg_replace') + '(' + quote + Regex(r'.*/e\b') + quote
    grammar.ignore(cppStyleComment)
    grammar.ignore(pythonStyleComment)

    return lang.generic_method(
        path=php_dest,
        gmmr=grammar,
        func=lang.parse,
        msgs={
            OPEN: 'Code may allow RCE using preg_replace()',
            CLOSED: 'Code does not allow RCE using preg_replace()',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)
