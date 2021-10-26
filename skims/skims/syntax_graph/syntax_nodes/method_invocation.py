from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_method_invocation_node(
    args: SyntaxGraphArgs, expr: str, expr_id: str, arguments_id: str
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expr,
        expression_id=expr_id,
        arguments_id=arguments_id,
        danger=False,
        label_type="MethodInvocation",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expr_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(arguments_id)),
        label_ast="AST",
    )

    return args.n_id
