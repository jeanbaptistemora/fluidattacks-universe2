from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Iterator,
)


def build_string_literal_node(
    args: SyntaxGraphArgs, value: str, c_ids: Iterator
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        value_type="string",
        label_type="Literal",
    )

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
