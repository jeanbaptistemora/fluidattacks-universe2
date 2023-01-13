from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_throw_node(
    args: SyntaxGraphArgs,
    expression_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="ThrowStatement",
    )

    if expression_id:
        args.syntax_graph.nodes[args.n_id]["expression_id"] = expression_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(expression_id)),
            label_ast="AST",
        )

    return args.n_id
