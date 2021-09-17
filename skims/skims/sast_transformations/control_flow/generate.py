from contextlib import (
    suppress,
)
from functools import (
    partial,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
)
from sast_transformations.control_flow.walkers import (
    WALKERS_BY_LANG,
)
from utils import (
    graph as g,
)


def _next_declaration(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    with suppress(IndexError):
        # check if a following stmt is pending in parent entry of the stack
        next_id = stack[-2].pop("next_id", None)

        # if there was a following stament, it does not have the current one
        # as child and they are not the same
        if (
            next_id
            and n_id != next_id
            and n_id not in g.adj_cfg(graph, next_id)
        ):
            # check that the next node is not already part of this cfg branch
            for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
                if statement == next_id:
                    break
            else:
                # add following statement to cfg
                graph.add_edge(n_id, next_id, **edge_attrs)


def generic(
    graph: Graph,
    n_id: str,
    stack: Stack,
    language: GraphShardMetadataLanguage,
    edge_attrs: EdgeAttrs,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs["label_type"]

    stack.append(dict(type=n_attrs_label_type))

    lang_generic = partial(generic, language=language)
    for walker in WALKERS_BY_LANG[language]:
        if n_attrs_label_type in walker.applicable_node_label_types:
            walker.walk_fun(graph, n_id, stack, lang_generic)
            break
    else:
        # if there is no walker for the expression, stop the recursion
        # the only thing left is to check if there is a cfg statement following
        _next_declaration(graph, n_id, stack, edge_attrs=edge_attrs)

    stack.pop()
