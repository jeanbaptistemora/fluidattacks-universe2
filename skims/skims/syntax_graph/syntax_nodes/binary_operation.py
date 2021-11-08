from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_binary_operation_node(
    args: SyntaxGraphArgs, operator: str, left_id: str, right_id: str
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        operator=operator,
        left_id=left_id,
        right_id=right_id,
        danger=False,
        evaluated=False,
        label_type="BinaryOperation",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(left_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(right_id)),
        label_ast="AST",
    )

    return args.n_id
