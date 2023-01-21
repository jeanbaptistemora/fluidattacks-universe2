from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Iterator,
    Optional,
)


def build_object_node(
    args: SyntaxGraphArgs, c_ids: Iterator[NId], name: Optional[str] = None
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Object",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["name"] = name

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
