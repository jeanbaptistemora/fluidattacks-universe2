from collections.abc import (
    Iterable,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_try_statement_node(
    args: SyntaxGraphArgs,
    block_node: NId,
    catch_blocks: Iterable[NId] | None,
    try_block: NId | None,
    resources_spec: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block_node,
        label_type="TryStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_node)),
        label_ast="AST",
    )

    if resources_spec:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(resources_spec)),
            label_ast="AST",
        )

    if catch_blocks:
        for c_id in catch_blocks:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(c_id)),
                label_ast="AST",
            )

    if try_block:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(try_block)),
            label_ast="AST",
        )

    return args.n_id
