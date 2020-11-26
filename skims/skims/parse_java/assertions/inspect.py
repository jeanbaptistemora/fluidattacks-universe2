# Standard library
from typing import (
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    method_declaration,
    types,
)
from utils.logs import (
    blocking_log,
)


def inspect(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
) -> types.Context:
    ctx: types.Context = {
        'inputs': {
            'vars': {},
        },
        'vars': {},
    }

    for n_id in path:
        n_attrs = graph.nodes[n_id]
        n_attrs_label_type = n_attrs['label_type']

        if n_attrs_label_type == 'MethodDeclaration':
            method_declaration.inspect(graph, n_id, ctx=ctx)
        else:
            blocking_log('warning', 'Unknown path %s after: %s', path, n_id)
            break

    return ctx
