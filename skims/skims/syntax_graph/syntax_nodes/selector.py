from collections.abc import (
    Iterator,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_selector_node(
    args: SyntaxGraphArgs,
    identifier: str | None,
    c_ids: Iterator[NId] | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Selector",
    )

    if identifier:
        args.syntax_graph.nodes[args.n_id]["selector_name"] = identifier

    if c_ids:
        for c_id in c_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(c_id)),
                label_ast="AST",
            )

    return args.n_id
