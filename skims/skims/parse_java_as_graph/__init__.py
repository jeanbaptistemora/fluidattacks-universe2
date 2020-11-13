# Standar libraries
from typing import (
    Any,
    Dict,
    Optional,
)

# Third party libraries
from networkx import DiGraph


def is_low_unity(model: Dict[str, Any]) -> bool:
    if not isinstance(model, dict):
        return False
    return {
        'c',
        'l',
        'text',
        'type',
    } == set(model.keys())


def from_model(
        model: Any,
        graph: DiGraph = DiGraph(),
        father_id: Optional[int] = None,
) -> DiGraph:
    if isinstance(model, dict):
        if is_low_unity(model):
            graph.add_node(id(model), **model)
        else:
            for key, value in model.items():
                node_key = id(value)
                graph.add_node(node_key, type=key)
                if father_id:
                    graph.add_edge(father_id, node_key)
                from_model(
                    model=value,
                    graph=graph,
                    father_id=node_key,
                )
    elif isinstance(model, list):
        for value in model:
            node_key = id(value)
            graph.add_node(node_key)
            graph.add_edge(father_id, node_key)
            from_model(model=value, graph=graph, father_id=node_key)
    return graph
