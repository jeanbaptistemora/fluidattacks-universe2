from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_member_access_node(
    args: SyntaxGraphArgs,
    member: str,
    expression: str,
    expression_id: str,
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        member=member,
        expression=expression,
        expression_id=expression_id,
        danger=False,
        label_type="MemberAccess",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression_id)),
        label_ast="AST",
    )

    return args.n_id
