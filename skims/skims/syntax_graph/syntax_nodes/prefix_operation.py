from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_prefix_node(
    args: SyntaxGraphArgs,
    prefix: str,
    expression_id: str,
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        prefix=prefix,
        expression_id=expression_id,
        danger=False,
        evaluated=False,
        label_type="PrefixOperation",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression_id)),
        label_ast="AST",
    )

    return args.n_id
