from contextlib import (
    suppress,
)
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
                "statement_block",
                "expression_statement",
                "program",
            },
            partial(step_by_step, _generic=_generic),
        ),
    )
    for types, walker in walkers:
        if n_attrs_label_type in types:
            walker(graph, n_id, stack)
            break
    else:
        with suppress(IndexError):
            if (
                (next_id := stack[-2].pop("next_id", None))
                and n_id != next_id
                and n_id not in g.adj_cfg(graph, next_id)
            ):
                for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
                    if statement == next_id:
                        break
                else:
                    graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def add(graph: Graph) -> None:
    _generic(graph, g.ROOT_NODE, stack=[], edge_attrs=ALWAYS)
