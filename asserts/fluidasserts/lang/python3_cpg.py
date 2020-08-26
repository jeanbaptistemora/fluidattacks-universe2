"""Fluid asserts Python3 parser."""

# Standar imports
from ast import parse, ClassDef
from typing import (Dict, List, Tuple)

# 3rd party imports
from networkx import DiGraph

# Local imports
from fluidasserts.utils.generic import get_paths_tree
from fluidasserts.lang import node_creator as creator
from fluidasserts.lang import GRAPHS

GRAPH: DiGraph = GRAPHS.get()


def _read(file_path, *args) -> str:
    """Read python file."""
    kwargs: Dict = {'encoding': 'iso-8859-1'}
    with open(file_path, *args, **kwargs) as file:
        return file.read()


def create_cpg(path: str, exclude: Tuple = None):
    """Create a CPG with the files that are inside the path."""
    paths = get_paths_tree(path, exclude, endswith=('.py'))
    if paths:
        principal_name = paths[0][0].split('/')[-1]
        paths = [(root, root[root.index(principal_name):], dirs, files)
                 for root, dirs, files in paths]

    for root, relative, _, files in paths:
        namespace_name = relative.replace('/', '.')
        for file in files:
            file_path = f'{root}/{file}'
            file_node = creator.file(GRAPH, name=file_path)

            if file != '__init__.py':
                module_name = f'{namespace_name}.{file.split(".py")[0]}'
                namespace_node = creator.namespace_block(
                    GRAPH, name=module_name, file_name=file_path)
            else:
                namespace_node = creator.namespace_block(
                    GRAPH,
                    name=namespace_name,
                    file_name=file_path)
            GRAPH.add_edge(file_node, namespace_node, type='AST')

            try:
                ast_ = parse(_read(file_path))
            except SyntaxError:
                continue
            kwargs = {'namespace_name': namespace_name,
                      'file': file_path, 'father': namespace_node}
            transform_body(ast_.body, **kwargs)


def transform_body(items: List, **kwargs):
    """Transform statement body."""
    for item in items:
        class_name = item.__class__.__name__.lower()
        globals()[f'transform_{class_name}'](item, **kwargs)


def transform_classdef(class_: ClassDef, **kwargs: Dict):
    """Convert a class statement in a node."""
    namespace_name = kwargs.get('namespace_name', '')
    ast_parent_type = kwargs.get('ast_parent_type', None)
    file_path = kwargs.get('file',)
    class_name = class_.name
    full_name = f'{namespace_name}.{class_name}'
    ast_parent_full_name = f'{file_path}.{full_name}'
    class_node = creator.type_decl(graph=GRAPH,
                                   name=class_name,
                                   full_name=full_name,
                                   ast_parent_type=ast_parent_type,
                                   ast_parent_full_name=ast_parent_full_name,
                                   line_number=class_.lineno,
                                   column_number=class_.col_offset,
                                   line_number_end=class_.end_lineno,
                                   column_number_end=class_.end_col_offset,
                                   file_name=file_path,
                                   order=kwargs.get('order', None))
    kwargs['father'] = class_node
    transform_body(class_.body, **kwargs)
