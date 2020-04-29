# -*- coding: utf-8 -*-

"""This module has helper functions for code analysis modules."""

# standard imports
import os
import re
from typing import Any, Callable, Dict, List, Tuple
from functools import lru_cache
from itertools import accumulate

# 3rd party imports
from pyparsing import ParserElement

# local imports
from fluidasserts import Unit
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.generic import get_paths


@lru_cache(maxsize=None, typed=True)
def _enum_and_accum(_iterable):
    return tuple(enumerate(accumulate(_iterable), start=1))


def _get_line_number(column: int, columns_per_line: List[int]) -> int:
    """
    Return the line number given you know the columns per line, and the column.

    :param column: Column number to be searched.
    :param cols_per_line: List of columns per line.
    """
    result: int = 0
    for line_no, cols_up_to_this_line in _enum_and_accum(columns_per_line):
        if cols_up_to_this_line > column:
            result = line_no
            break
    return result


def _remove_accepted(line_numbers, lines):
    """
    Remove vulnerable lines marked with # nosec from results.

    :param line_numbers: vulnerable line numbers
    :param lines: file lines to search for flag in
    """
    regex = re.compile(r'(#|//) nosec')
    for line in sorted(line_numbers, reverse=True):
        if regex.search(lines[line - 1]):
            line_numbers.remove(line)


def parse_single(grammar: ParserElement,
                 path: str) -> Tuple[List[Unit], List[Unit]]:
    """
    Return a tuple with the results of parsing path with grammar.

    the left element contains the matched results,
    the right element contains the results that didn't match.

    :param grammar: Grammar to be searched for in path.
    :param path: Path to the destination file.
    """
    with open(path, encoding='latin-1') as file_d:
        lines = file_d.read().splitlines()

    lines_length = tuple(map(lambda x: len(x) + 1, lines))
    file_as_string = '\n'.join(lines)

    # Given scanString expands tabs to 'n' number of spaces
    # And we count tabs as '1' char width
    # And scanString reports the match column relative to the expanded version
    # When a file contains tabs
    # Then the line numbers will get an offset
    # Given we force to parse without expanding tabs
    grammar.parseWithTabs()
    # Then the line numbers are reported correctly

    line_numbers = [
        _get_line_number(start, lines_length)
        for _, start, _ in grammar.scanString(file_as_string)]

    _remove_accepted(line_numbers, lines)

    results: List[Unit] = [Unit(where=path,
                                source='Lines',
                                specific=list(dict.fromkeys(line_numbers)),
                                fingerprint=get_sha256(path))]

    return (results, []) if line_numbers else ([], results)


def parse(grammar: ParserElement,
          path: str,
          lang_spec: dict,
          exclude: list = None) -> Tuple[List[Unit], List[Unit]]:
    """
    Return a tuple with the results of parsing path with grammar.

    the left element contains the matched results,
    the right element contains the results that didn't match.

    :param grammar: Grammar to be searched for in path.
    :param path: Path to the destination file.
    :param lang_spec: Contains language-specific syntax elements, such as
                      acceptable file extensions and comment delimiters.
    """
    matched, not_matched = [], []
    exclude = tuple(exclude) if exclude else tuple()
    extensions = lang_spec.get('extensions')
    for full_path in get_paths(path, endswith=extensions, exclude=exclude):
        _matched, _not_matched = parse_single(grammar, full_path)
        matched.extend(_matched)
        not_matched.extend(_not_matched)

    return matched, not_matched


def generic_method(path: str,
                   gmmr: Any,
                   func: Callable,
                   msgs: Dict[str, str],
                   excl: list = None,
                   spec: dict = None,
                   reverse: bool = False) -> tuple:
    """Check grammar in a destination and propagate results upwards."""
    if not os.path.exists(path):
        return UNKNOWN, 'File does not exist'

    excl = excl if excl else []
    spec = spec if spec else {}

    if reverse:
        safes, vulns = func(gmmr, path, spec, excl)
    else:
        vulns, safes = func(gmmr, path, spec, excl)

    if vulns:
        return OPEN, msgs[OPEN], vulns, safes
    if safes:
        return CLOSED, msgs[CLOSED], vulns, safes
    return CLOSED, 'No files were tested'
