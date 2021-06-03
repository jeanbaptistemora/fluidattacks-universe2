from functools import (
    partial,
)
from model.graph_model import (
    Graph,
)
from sast_transformations import (
    ALWAYS,
)
from sast_transformations.control_flow.common import (
    link_to_last_node,
    step_by_step,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
)
from utils import (
    graph as g,
)


def _generic(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs["label_type"]
    stack.append(dict(type=n_attrs_label_type))

    walkers = (
        (
            {
                "block",
            },
            partial(step_by_step, _generic=_generic),
        ),
        (
            {"function_declaration", "method_declaration"},
            partial(link_to_last_node, _generic=_generic),
        ),
    )
    for types, walker in walkers:
        if n_attrs_label_type in types:
            walker(graph, n_id, stack)
            break
    else:
        if (next_id := stack[-2].pop("next_id", None)) and n_id != next_id:
            graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return g.pred_has_labels(label_type="function_declaration")(
            n_id
        ) or g.pred_has_labels(label_type="method_declaration")(n_id)

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        _generic(graph, n_id, stack=[], edge_attrs=ALWAYS)
