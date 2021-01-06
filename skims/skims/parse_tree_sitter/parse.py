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
from parse_tree_sitter.transformations.control_flow import (
    add as add_control_flow,
)
from parse_tree_sitter.transformations.styles import (
    add as add_styles,
)
from state import (
    STATE_FOLDER,
)
from utils.ctx import (
    CTX,
    TREE_SITTER_JAVA,
)
from utils.graph import (
    copy_ast2,
    copy_cfg2,
    to_svg,
)
from utils.string import (
    get_debug_path,
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
            label_c=obj.start_point[1],
            label_l=obj.start_point[0],
            label_parent_ast=_parent,
            label_type=obj.type,
        )

        if _parent is not None:
            _graph.add_edge(
                _parent,
                n_id,
                label_ast='AST',
                label_index=_edge_index,
            )

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
    path: str,
) -> nx.DiGraph:
    raw_tree: Tree = parser.parse(content)

    graph: nx.DiGraph = _build_ast_graph(raw_tree)
    add_control_flow(graph)
    add_styles(graph)

    if CTX.debug:
        output = get_debug_path('tree-sitter-' + path)
        to_svg(graph, output)
        to_svg(copy_ast2(graph), f'{output}.ast')
        to_svg(copy_cfg2(graph), f'{output}.cfg')

    return graph
