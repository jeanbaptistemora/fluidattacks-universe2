"""Fluid asserts Python3 parser."""

# Standar imports
from typing import (Dict, List, Tuple)

# 3rd party imports
from lark import Lark
from lark import Transformer
from lark.indenter import Indenter
from networkx import DiGraph

# Local imports
from fluidasserts.utils.generic import get_paths_tree
from fluidasserts.lang import node_creator as creator


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


def _create_namespaces(graph: DiGraph, paths: List[Tuple]):
    for root, relative, _, files in paths:
        if '__init__.py' in files:
            namespace_name = relative.split('/')[-1]
            creator.namespace_block(
                graph,
                name=namespace_name,
                full_name=f'{root}/__init__.py:{namespace_name}',
                file_name=f'{root}/__init__.py')
            for file in files:
                creator.file(graph, name=f'{root}/{file}')


def create_cpg(graph: DiGraph, path: str, exclude: Tuple = None):
    """Create a CPG with the files that are inside the path."""
    paths = get_paths_tree(path, exclude, endswith=('py'))
    if paths:
        principal_name = paths[0][0].split('/')[-1]
        paths = [(root, root[root.index(principal_name):], dirs, files)
                 for root, dirs, files in paths]
    _create_namespaces(graph, paths)


def parse(file_path: str):
    """Convert a python file to a graph."""
    kwargs: Dict = dict(
        rel_to=__file__, postlex=PythonIndenter(), start='file_input')

    python_parser3 = Lark.open('python3.lark', parser='lalr', **kwargs)
    python_parser3.parse(_read(file_path))
