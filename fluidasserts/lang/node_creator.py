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


def namespace_block(graph: DiGraph, name: str, full_name: str, file_name: str):
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
