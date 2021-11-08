from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_string_literal_node(args: SyntaxGraphArgs, value: str) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        value_type="string",
        danger=False,
        evaluated=False,
        label_type="Literal",
    )

    return args.n_id
