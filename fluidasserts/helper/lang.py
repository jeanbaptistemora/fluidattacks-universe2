# -*- coding: utf-8 -*-

"""This module has helper functions for code analysis modules."""

# standard imports
import os
import re
from typing import Any, Callable, Dict, List, Tuple
from functools import lru_cache
from itertools import accumulate

# 3rd party imports
from androguard.misc import AnalyzeAPK
from pyparsing import ParserElement, ParseException, ParseResults

# local imports
from fluidasserts import Unit
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.generic import get_paths


def _re_compile(
        literals: tuple,
        pre: str = r'',
        suf: str = r'',
        sep: str = r''):
    """Return a compiled regular expression from a tuple of literals."""
    return re.compile(f'{pre}(?:{sep.join(map(re.escape, literals))}){suf}')


@lru_cache(maxsize=None, typed=True)
def _enum_and_accum(_iterable):
    return tuple(enumerate(accumulate(_iterable), start=1))


def _is_empty_result(parse_result: ParseResults) -> bool:
    """
    Check if a ParseResults is empty.

    :param parse_result: ParseResults from pyparsing.
    """
    if isinstance(parse_result, ParseResults):
        if parse_result:
            return _is_empty_result(parse_result[0])
        return True
    return not bool(parse_result)


@lru_cache(maxsize=None, typed=True)
def _non_commented_code(code_file: str, lang_spec: tuple) -> tuple:
    """
    Walk through the file and discard comments.

    :param code_file: Source code file to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                      acceptable file extensions and comment delimiters.
    :return: Tuple of non-commented (line number, line content) file contents.
    """
    lang_spec = dict(lang_spec)
    # As much tokens as needed like in PHP ('#', '//')
    line_start = lang_spec.get('line_comment')
    # Just one token like in C '/*' or in HTML '<!--'
    block_beg = lang_spec.get('block_comment_start')
    # Just one token like in C '*/' or in HTML '-->'
    block_end = lang_spec.get('block_comment_end')

    with open(code_file, encoding='latin-1') as file_descriptor:
        file_as_str = '\n'.join(file_descriptor.read().splitlines())

    replacements = []
    if block_beg and block_end:
        if len(block_end) == 2:
            beg = re.escape(block_beg)
            end1, end2 = map(re.escape, block_end)
            replacements.append((
                f'({beg}(?:[^{block_end[0]}]|{end1}(?!{end2}))*{end1}{end2})'))
        else:
            replacements.append(f'((?={block_beg})(?:[\\s\\S]*?){block_end})')
    if line_start:
        tokens = (f'(?:{x})' for x in map(re.escape, line_start))
        replacements.append(f'((?:{"|".join(tokens)})(?:\\\\\\n|[^\\n])*)')

    for regex in replacements:
        file_as_str = re.sub(
            regex,
            lambda x: '\n' * x[0].count('\n'),
            file_as_str)

    return tuple(
        (num, line)
        for num, line in enumerate(file_as_str.splitlines(), start=1)
        if line.strip())


def _get_match_lines(
        grammar: ParserElement,
        code_file: str,
        lang_spec: dict) -> List[int]:  # noqa
    """
    Check grammar in file.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_file: Source code file to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                       acceptable file extensions and comment delimiters.
    :return: List of lines that contain grammar matches.
    """
    affected_lines = []
    # We need hashable arguments
    lang_spec_hashable = tuple(lang_spec.items())
    for line_number, line_content in _non_commented_code(
            code_file, lang_spec_hashable):
        try:
            results = grammar.searchString(line_content, maxMatches=1)
            if not _is_empty_result(results):
                affected_lines.append(line_number)
        except ParseException:
            pass
    return affected_lines


def _get_line_number(column: int, columns_per_line: List[int]) -> int:
    """
    Return the line number given you know the columns per line, and the column.

    :param column: Column number to be searched.
    :param cols_per_line: List of columns per line.
    """
    for line_no, cols_up_to_this_line in _enum_and_accum(columns_per_line):
        if cols_up_to_this_line > column:
            return line_no
    # This return is not going to happen, but if it happens, then be prepared
    return 0


@lru_cache(maxsize=None, typed=True)
def _path_match_extension(path: str, extensions: tuple) -> bool:
    """
    Return True if the provided path ends with any of the provided extensions.

    :param path: Path which extension is to be matched with extensions.
    :param extensions: Tuple of extensions, or None.
    """
    if not extensions:
        return True
    return path.endswith(extensions)


def lists_as_string(lists: List[List], result: ParseResults,
                    level: int) -> str:
    """
    Format ParseResults as string.

    :param lists: Nested Lists from ParseResults.
    :param result: Results from parsing.
    :param level: Depth level to control recursion.
    """
    for lst in lists:
        if isinstance(lst, list):
            result = lists_as_string(lst, result, level + 1)
        else:
            result += "\t" * int(level / 2) + lst + "\n"
    return result


def _path_contains_grammar(grammar: ParserElement, path: str) -> dict:
    """
    Return a dict mapping the path to the lines where the grammar matched.

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

    matched_lines = [
        _get_line_number(start, lines_length)
        for _, start, _ in grammar.scanString(file_as_string)]

    if matched_lines:
        return {
            path: {
                'lines': str(matched_lines)[1:-1],
                'sha256': get_sha256(path),
            }
        }
    return {}


def _path_contains_grammar2(
        grammar: ParserElement, path: str) -> Tuple[List[Unit], List[Unit]]:
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

    lines = [
        _get_line_number(start, lines_length)
        for _, start, _ in grammar.scanString(file_as_string)]

    results: List[Unit] = [Unit(where=path,
                                source='Lines',
                                specific=lines,
                                fingerprint=get_sha256(path))]

    return (results, []) if lines else ([], results)


def path_contains_grammar(
        grammar: ParserElement, path: str,
        lang_spec: dict, exclude: list = None) -> List[str]:
    """
    Return a dict mapping all files in path to the line with grammar matches.

    :param grammar: Grammar to be searched for in path.
    :param path: Path to the destination file.
    :param lang_spec: Contains language-specific syntax elements, such as
                      acceptable file extensions and comment delimiters.
    """
    vulns = {}
    exclude = tuple(exclude) if exclude else tuple()
    extensions = lang_spec.get('extensions')
    for path in get_paths(path, endswith=extensions, exclude=exclude):
        vulns.update(_path_contains_grammar(grammar, path))
    return vulns


def path_contains_grammar2(
        grammar: ParserElement,
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
        _matched, _not_matched = \
            _path_contains_grammar2(grammar, full_path)
        matched.extend(_matched)
        not_matched.extend(_not_matched)

    return matched, not_matched


def block_contains_grammar(grammar: ParserElement, code_dest: str,
                           lines: List[str],
                           get_block_fn: Callable,
                           should_have: str = '',
                           should_not_have: str = '',
                           search_for_empty: bool = False) -> List[str]:
    """
    Check block grammar.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_dest: Source code file to check.
    :param lines: List of starting lines.
    :param get_block_fn: Function that gives block code starting at line.
    :param should_have: A string to search for in the match results.
    :param should_not_have: A string to search for in the match results.
    """
    vulns = {}
    vuln_lines = []
    if should_have:
        should_have_re = re.compile(should_have, flags=re.M)
    if should_not_have:
        should_not_have_re = re.compile(should_not_have, flags=re.M)
    with open(code_dest, encoding='latin-1') as code_f:
        file_lines = code_f.read().splitlines()
    for line in map(int, lines.split(',')):
        txt = get_block_fn(file_lines, line)
        results = grammar.searchString(txt, maxMatches=1)
        results_str = str(results)

        is_vulnerable = not search_for_empty
        if _is_empty_result(results):
            is_vulnerable = search_for_empty
        elif should_have and should_have_re.search(results_str):
            is_vulnerable = search_for_empty
        elif should_not_have and should_not_have_re.search(results_str):
            is_vulnerable = search_for_empty

        if is_vulnerable:
            vuln_lines.append(line)

    if vuln_lines:
        vulns = {
            code_dest: {
                'lines': str(vuln_lines)[1:-1],
                'sha256': get_sha256(code_dest),
            }
        }
    return vulns


def block_contains_empty_grammar(grammar: ParserElement, code_dest: str,
                                 lines: List[str],
                                 get_block_fn: Callable,
                                 should_have: str = '',
                                 should_not_have: str = '') -> List[str]:
    """
    Check empty block grammar.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_dest: Source code file to check.
    :param lines: List of starting lines.
    :param get_block_fn: Function that gives block code starting at line.
    :param should_have: A string to search for in the match results.
    :param should_not_have: A string to search for in the match results.
    """
    return block_contains_grammar(grammar,
                                  code_dest,
                                  lines,
                                  get_block_fn,
                                  should_have=should_have,
                                  should_not_have=should_not_have,
                                  search_for_empty=True)


def _check_grammar_in_file(grammar: ParserElement, code_dest: str,
                           lang_spec: dict) -> Dict[str, List[str]]:
    """
    Check grammar in file.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_dest: File or directory to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                       acceptable file extensions and comment delimiters.
    :param exclude: Exclude files or directories with given strings
    :return: Maps files to their found vulnerabilites.
    """
    vulns = {}
    lines = []
    lang_extensions = lang_spec.get('extensions')

    if lang_extensions:
        if _path_match_extension(code_dest, lang_extensions):
            lines = _get_match_lines(grammar, code_dest, lang_spec)
    else:
        lines = _get_match_lines(grammar, code_dest, lang_spec)
    if lines:
        vulns[code_dest] = {
            'lines': str(lines)[1:-1],
            'sha256': get_sha256(code_dest),
        }
    return vulns


def _check_grammar_in_dir(grammar: ParserElement, code_dest: str,
                          lang_spec: dict,
                          exclude: list = None) -> Dict[str, List[str]]:
    """
    Check grammar in directory.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_dest: File or directory to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                       acceptable file extensions and comment delimiters.
    :param exclude: Exclude files or directories with given strings
    :return: Maps files to their found vulnerabilites.
    """
    exclude = tuple(exclude) if exclude else tuple()
    vulns = {}
    for full_path in get_paths(code_dest, exclude=exclude):
        vulns.update(_check_grammar_in_file(grammar, full_path, lang_spec))
    return vulns


def check_grammar(grammar: ParserElement, code_dest: str,
                  lang_spec: dict,
                  exclude: list = None) -> Dict[str, List[str]]:
    """
    Check grammar in location.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_dest: File or directory to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                       acceptable file extensions and comment delimiters.
    :param exclude: Exclude files or directories with given strings
    :return: Maps files to their found vulnerabilites.
    """
    if not exclude:
        exclude = []
    vulns = {}
    if os.path.isdir(code_dest):
        vulns = _check_grammar_in_dir(grammar, code_dest, lang_spec, exclude)
    else:
        vulns = _check_grammar_in_file(grammar, code_dest, lang_spec)
    return vulns


def check_grammar2(grammar: ParserElement,
                   code_dest: str,
                   lang_spec: dict,
                   exclude: list = None) -> Tuple[List[Unit], List[Unit]]:
    """
    Check grammar in location.

    :param grammar: Pyparsing grammar against which file will be checked.
    :param code_dest: File or directory to check.
    :param lang_spec: Contains language-specific syntax elements, such as
                       acceptable file extensions and comment delimiters.
    :param exclude: Exclude files or directories with given strings
    :return: Maps files to their found vulnerabilites.
    """
    matched, not_matched = [], []
    exclude = tuple(exclude) if exclude else tuple()
    extensions = lang_spec.get('extensions')
    for full_path in get_paths(
            code_dest, exclude=exclude, endswith=extensions):
        lines = _get_match_lines(grammar, full_path, lang_spec)

        results: List[Unit] = [Unit(where=full_path,
                                    source='Lines',
                                    specific=lines,
                                    fingerprint=get_sha256(full_path))]

        _matched, _not_matched = (results, []) if lines else ([], results)

        matched.extend(_matched)
        not_matched.extend(_not_matched)

    return matched, not_matched


def generic_method(path: str,
                   gmmr: Any,
                   func: Callable,
                   msgs: Dict[str, str],
                   excl: list = None,
                   spec: dict = None) -> tuple:
    """Check grammar in a destination and propagate results upwards."""
    if not os.path.exists(path):
        return UNKNOWN, 'File does not exist'

    excl = excl if excl else []
    spec = spec if spec else {}

    vulns, safes = func(gmmr, path, spec, excl)

    if vulns:
        return OPEN, msgs[OPEN], vulns, safes
    if safes:
        return CLOSED, msgs[CLOSED], vulns, safes
    return CLOSED, 'No files were tested'


@lru_cache(maxsize=None, typed=True)
def analyze_apk(path: str) -> tuple:
    """Return the resultant objects after analyzing the apk."""
    return AnalyzeAPK(path)
