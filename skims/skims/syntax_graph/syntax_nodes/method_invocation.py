from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_method_invocation_node(
    args: SyntaxGraphArgs, expr: str, expr_id: str, arguments_id: Optional[str]
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expr,
        expression_id=expr_id,
        label_type="MethodInvocation",
    )

    if arguments_id:
        args.syntax_graph.nodes[args.n_id]["arguments_id"] = arguments_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(arguments_id)),
            label_ast="AST",
        )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expr_id)),
        label_ast="AST",
    )

    return args.n_id
