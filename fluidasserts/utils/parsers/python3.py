"""Fluid asserts Python3 parser."""

# Standar imports
from typing import (Dict, List)

# 3rd party imports
from lark import Lark
from lark import Transformer
from lark.indenter import Indenter


class PythonIndenter(Indenter):
    """Python 3 indenter."""
    NL_type: str = '_NEWLINE'
    OPEN_PAREN_types: List[str] = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types: List[str] = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type: str = '_INDENT'
    DEDENT_type: str = '_DEDENT'
    tab_len: int = 4


class TreeToJson(Transformer):  # pylint: disable=too-few-public-methods
    """Convert Tree Lark in a Graph Nodes."""


def _read(file_path, *args) -> str:
    """Read python file."""
    kwargs: Dict = {'encoding': 'iso-8859-1'}
    with open(file_path, *args, **kwargs) as file:
        return file.read()


def parse(file_path: str):
    """Convert a python file to a graph."""
    kwargs: Dict = dict(
        rel_to=__file__, postlex=PythonIndenter(), start='file_input')

    python_parser3 = Lark.open('python3.lark', parser='lalr', **kwargs)
    python_parser3.parse(_read(file_path))
