from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_if_node(
    args: SyntaxGraphArgs,
    condition_id: str,
    true_id: str,
    false_id: Optional[str],
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        condition_id=condition_id,
        true_id=true_id,
        danger=False,
        label_type="If",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(condition_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(true_id)),
        label_ast="AST",
    )

    if false_id:
        args.syntax_graph.nodes[args.n_id]["false_id"] = false_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(false_id)),
            label_ast="AST",
        )

    return args.n_id
