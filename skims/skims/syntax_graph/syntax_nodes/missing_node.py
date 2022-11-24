from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Iterator,
)


def build_missing_node(
    args: SyntaxGraphArgs, n_type: str, c_ids: Iterator[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="MissingNode",
        node_type=n_type,
    )

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
