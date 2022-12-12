from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    List,
    Optional,
)


def build_class_node(
    args: SyntaxGraphArgs,
    name: str,
    block_id: NId,
    attrl_ids: Optional[List[NId]],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        block_id=block_id,
        label_type="Class",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    if attrl_ids:
        for n_id in attrl_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(n_id)),
                label_ast="AST",
            )

    return args.n_id
