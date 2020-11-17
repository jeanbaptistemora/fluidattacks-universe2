# Standar libraries
from typing import (
    Any,
    Tuple,
)

# Third party libraries
import networkx as nx

# Local import
from utils.graph import (
    has_label,
)


def get_successors_by_label(
    graph: nx.OrderedDiGraph,
    source: Any,
    *labels: Any,
    depth_limit: int = 1,
) -> Tuple[Any, ...]:
    return tuple(successor for _, successors in nx.dfs_successors(
        graph,
        source=source,
        depth_limit=depth_limit,
    ).items() for successor in successors if has_label(
        graph.nodes[successor],
        *labels,
    ))


def apply_control_flow_graph(graph: nx.OrderedDiGraph) -> nx.OrderedDiGraph:
    for node_id, node in graph.nodes.items():
        if has_label(node, 'IfThenStatement'):
            # an ifThenStatement should only have one Statement
            true_statement = get_successors_by_label(
                graph,
                node_id,
                'Statement',
                depth_limit=2,
            )[0]
            graph.add_edge(
                node_id,
                true_statement,
                label_cfg='CFG',
                label_true='True',
                color='red',
                label='True',
            )
        elif has_label(node, 'IfThenElseStatement'):
            true_statement = get_successors_by_label(
                graph,
                node_id,
                'StatementNoShortIf',
                depth_limit=2,
            )[0]
            graph.add_edge(
                node_id,
                true_statement,
                label_cfg='CFG',
                label_true='True',
                color='red',
                label='True',
            )
            false_statement = get_successors_by_label(
                graph,
                node_id,
                'Statement',
                depth_limit=2,
            )[0]
            graph.add_edge(
                node_id,
                false_statement,
                label_cfg='CFG',
                label_false='False',
                color='red',
                label='False',
            )

    return graph
