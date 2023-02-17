from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_method_invocation_node(
    args: SyntaxGraphArgs,
    expr: str,
    expr_id: Optional[NId],
    arguments_id: Optional[NId],
    object_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expr,
        expression_id=expr_id,
        label_type="MethodInvocation",
    )

    if object_id:
        args.syntax_graph.nodes[args.n_id]["object_id"] = object_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(object_id)),
            label_ast="AST",
        )

    if expr_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(expr_id)),
            label_ast="AST",
        )

    if arguments_id:
        args.syntax_graph.nodes[args.n_id]["arguments_id"] = arguments_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(arguments_id)),
            label_ast="AST",
        )

    return args.n_id
