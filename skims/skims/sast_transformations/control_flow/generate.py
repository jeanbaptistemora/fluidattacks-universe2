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
    CfgArgs,
    EdgeAttrs,
    Stack,
)
from sast_transformations.control_flow.walkers import (
    WALKERS_BY_LANG,
)
from utils import (
    graph as g,
)


def _next_declaration(args: CfgArgs, stack: Stack) -> None:
    with suppress(IndexError):
        # check if a following stmt is pending in parent entry of the stack
        next_id = stack[-2].pop("next_id", None)

        # if there was a following stament, it does not have the current one
        # as child and they are not the same
        if (
            next_id
            and args.n_id != next_id
            and args.n_id not in g.adj_cfg(args.graph, next_id)
        ):
            # check that the next node is not already part of this cfg branch
            for statement in g.pred_cfg_lazy(args.graph, args.n_id, depth=-1):
                if statement == next_id:
                    break
            else:
                # add following statement to cfg
                args.graph.add_edge(args.n_id, next_id, **args.edge_attrs)


def args_generic(args: CfgArgs, stack: Stack) -> None:
    node_type = args.graph.nodes[args.n_id]["label_type"]

    stack.append(dict(type=node_type))

    lang_generic = partial(generic, language=args.language)
    for walker in WALKERS_BY_LANG[args.language]:
        if node_type in walker.applicable_node_label_types:
            walker.walk_fun(args.graph, args.n_id, stack, lang_generic)
            break
    else:
        # if there is no walker for the expression, stop the recursion
        # the only thing left is to check if there is a cfg statement following
        _next_declaration(args, stack)

    stack.pop()


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
        args = CfgArgs(args_generic, graph, n_id, language, edge_attrs)
        _next_declaration(args, stack)

    stack.pop()
