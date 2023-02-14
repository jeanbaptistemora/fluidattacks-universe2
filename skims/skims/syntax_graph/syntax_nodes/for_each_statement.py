from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_for_each_statement_node(
    args: SyntaxGraphArgs,
    var_node: NId,
    iterable_item: NId,
    block_id: Optional[NId],
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        iterable_item_id=iterable_item,
        variable_id=var_node,
        label_type="ForEachStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(iterable_item)),
        label_ast="AST",
    )
    if block_id:
        args.syntax_graph.nodes[args.n_id]["block_id"] = block_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_id)),
            label_ast="AST",
        )

    return args.n_id
