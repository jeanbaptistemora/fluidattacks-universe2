# Standard library
from itertools import (
    count,
)
import os
from typing import (
    Any,
    Iterator,
    Optional,
)

# Third party libraries
import networkx as nx
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)

# Local libraries
from state import (
    STATE_FOLDER,
)
from utils.ctx import (
    TREE_SITTER_JAVA,
)

# Constants
LANGUAGES_SO = os.path.join(STATE_FOLDER, 'languages.so')

# Side effects
Language.build_library(LANGUAGES_SO, [
    TREE_SITTER_JAVA,
])

# Constants
PARSER_JAVA: Parser = Parser()
PARSER_JAVA.set_language(Language(LANGUAGES_SO, 'java'))


def _build_ast_graph(
    obj: Any,
    *,
    _counter: Optional[Iterator[int]] = None,
    _edge_index: Optional[int] = None,
    _graph: Optional[nx.DiGraph] = None,
    _parent: Optional[int] = None,
) -> nx.DiGraph:
    # Handle first level of recurssion, where _graph is None
    _counter = count(1) if _counter is None else _counter
    _graph = nx.DiGraph() if _graph is None else _graph

    if isinstance(obj, Tree):
        _graph = _build_ast_graph(obj.root_node)

    elif isinstance(obj, Node):
        if obj.has_error:
            raise ValueError()

        n_id = next(_counter)

        _graph.add_node(
            n_id,
            c=obj.start_point[1],
            l=obj.start_point[0],
            parent=_parent,
            type=obj.type,
        )

        if _parent is not None:
            _graph.add_edge(_parent, n_id, index=_edge_index, type='AST')

        for edge_index, child in enumerate(obj.children):
            _build_ast_graph(
                child,
                _counter=_counter,
                _edge_index=edge_index,
                _graph=_graph,
                _parent=n_id,
            )

    else:
        raise NotImplementedError()

    return _graph


def parse(
    *,
    content: bytes,
    parser: Parser,
) -> nx.DiGraph:
    raw_tree: Tree = parser.parse(content)

    graph: nx.DiGraph = _build_ast_graph(raw_tree)

    return graph
