from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Iterator,
)


def build_execution_block_node(
    args: SyntaxGraphArgs, c_ids: Iterator[str]
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        danger=False,
        label_type="ExecutionBlock",
    )

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
