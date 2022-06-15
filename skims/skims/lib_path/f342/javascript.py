from itertools import (
    accumulate,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    cppStyleComment,
    Keyword,
    nestedExpr,
    ParserElement,
    QuotedString,
)
import re
from typing import (
    Iterator,
    List,
    Tuple,
)

# 'anything'
L_CHAR = QuotedString("'")
# "anything"
L_STRING = QuotedString('"')


def _enum_and_accum(_iterable: List[int]) -> tuple:
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


def _remove_accepted(line_numbers: List[int], lines: List[str]) -> None:
    """
    Remove vulnerable lines marked with # nosec from results.

    :param line_numbers: vulnerable line numbers
    :param lines: file lines to search for flag in
    """
    regex = re.compile(r"(#|//) nosec")
    for line in sorted(line_numbers, reverse=True):
        if regex.search(lines[line - 1]):
            line_numbers.remove(line)


def parse_single(grammar: ParserElement, content: str) -> List[int]:
    """
    Return a tuple with the results of parsing path with grammar.

    the left element contains the matched results,
    the right element contains the results that didn't match.

    :param grammar: Grammar to be searched for in path.
    :param path: Path to the destination file.
    """
    lines = content.splitlines()

    lines_length = list(map(lambda x: len(x) + 1, lines))
    file_as_string = "\n".join(lines)

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
        for _, start, _ in grammar.scanString(file_as_string)
    ]

    _remove_accepted(line_numbers, lines)
    if line_numbers:
        return list(set(line_numbers))
    return []


def uses_console_log(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        """
        Search for ``console.log()`` calls in a JavaScript file or directory.

        :param js_dest: Path to a JavaScript source file or directory.
        :param exclude: Paths that contains any string from this list
        are ignored.
        :rtype: :class:`fluidasserts.Result`
        """
        grammar = Keyword("console") + "." + Keyword("log") + nestedExpr()
        grammar.ignore(cppStyleComment)
        grammar.ignore(L_STRING)
        grammar.ignore(L_CHAR)
        lines = parse_single(grammar, content)
        if lines:
            for line in lines:
                column: int = 0
                yield int(line), column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f342.uses_console_log",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.JS_USES_CONSOLE_LOG,
    )
