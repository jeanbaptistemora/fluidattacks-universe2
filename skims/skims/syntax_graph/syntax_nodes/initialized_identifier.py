from collections.abc import (
    Iterator,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_initialized_identifier_node(
    args: SyntaxGraphArgs,
    name: str | None,
    expr_id: NId | None,
    c_ids: Iterator[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="InitializedIdentifier",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["variable"] = name

    if expr_id:
        args.syntax_graph.nodes[args.n_id]["expression_id"] = expr_id

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
