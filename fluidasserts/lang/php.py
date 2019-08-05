# -*- coding: utf-8 -*-

"""This module allows to check PHP code vulnerabilities."""

# standard imports
# None

# 3rd party imports
from pyparsing import Keyword, oneOf, Regex

# local imports
from fluidasserts import Result
from fluidasserts import HIGH
from fluidasserts import OPEN, CLOSED
from fluidasserts.helper import lang
from fluidasserts.utils.decorators import api


LANGUAGE_SPECS = {
    'extensions': ('php', 'php4', 'php5', 'php6', 'php7',),
    'block_comment_start': '/*',
    'block_comment_end': '*/',
    'line_comment': ('#', '//',)
}  # type: dict


@api(risk=HIGH)
def has_preg_ce(php_dest: str, exclude: list = None) -> Result:
    """
    Search for preg_replace calls with '/e'.

    :param php_dest: Path to a PHP script or package.
    :param exclude: Paths that contains any string from this list are ignored.
    """
    quote = oneOf(["'", '"'])
    grammar = Keyword('preg_replace') + '(' + quote + Regex(r'.*/e\b') + quote

    return lang.generic_method(
        path=php_dest,
        gmmr=grammar,
        func=lang.path_contains_grammar2,
        msgs={
            OPEN: 'Code may allow RCE using preg_replace()',
            CLOSED: 'Code does not allow RCE using preg_replace()',
        },
        spec=LANGUAGE_SPECS,
        excl=exclude)
