"""Fluidasserts lang module to create gra[h nodes."""
# pylint: disable=unused-argument

# Standar imports
from typing import Dict

# 3rd party imports
from networkx import DiGraph


def _create_node(graph: DiGraph, **kwargs: Dict):
    node_id = id(kwargs)
    graph.add_node(node_id, **kwargs)
    return node_id


def meta_data(graph: DiGraph, language: str, version: str = None) -> int:
    """
    Node to save meta data about the graph on its properties.

    Exactly one node of this type per graph.

    :param language: The programming language this graph originates from.
    :param version: A version.
    """
    args = locals()
    args.pop('graph')
    args['type'] = 'META_DATA'
    return _create_node(graph, **args)


def file(graph: DiGraph, name: str):
    """
    Node representing a source file. Often also the AST root.

    :param name: Name of represented file
    """
    args = locals()
    args.pop('graph')
    args['type'] = 'FILE'
    return _create_node(graph, **args)


def namespace_block(graph: DiGraph,
                    name: str,
                    file_name: str,
                    full_name: str = None):
    """
    A reference to a namespace.

    :param name: Name of represented namespace.
    :param full_name: Full name of namaspace, must include in file name and
      package name In theory, the FULL_NAME just needs to be unique and is used
      for linking references. In practice, this should be human readable
    :param file_name: Full path of file that contained this node, will be
      linked into corresponding FILE nodes.
    """
    args = locals()
    args.pop('graph')
    args['type'] = 'NAMESPACE_BLOCK'
    return _create_node(graph, **args)


def type_decl(graph: DiGraph,
              name: str,
              full_name: str,
              ast_parent_type: str,
              ast_parent_full_name: str,
              line_number: int,
              column_number: int,
              line_number_end: int,
              column_number_end: int,
              file_name: str,
              order: int = None,
              ):
    """
    A type declaration
    :param name: Name of represented type.
    :param full_name: Full name of type, must include package name directory.
    :param ast_parent_type: The type of the AST parent. Since this is
      only used in some parts of the graph.
    :param ast_parent_full_name: The FULL_NAME of a the AST parent of an
      entity.
    :param line_number: Line where the code starts.
    :param column_number: Column where the code starts.
    :param line_number_end: Line where the code ends.
    :param column_number_end: Column where the code ends.
    :param order: The ordering has no technical meaning, but is used for
      pretty printing and OUGHT TO reflect order in the source code.
    :param file_name: Full path of file that contained this node, will be
      linked into corresponding FILE nodes.
    """
    args = locals()
    args.pop('graph')
    args['type'] = 'TYPE_DECL'
    return _create_node(graph, **args)
