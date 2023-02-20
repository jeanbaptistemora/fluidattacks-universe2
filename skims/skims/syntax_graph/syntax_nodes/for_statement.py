from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_for_statement_node(
    args: SyntaxGraphArgs,
    initializer_node: NId | None,
    condition_node: NId | None,
    update_node: NId | None,
    body_node: NId | None,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        label_type="ForStatement",
    )

    if initializer_node:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(initializer_node)),
            label_ast="AST",
        )

    if condition_node:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(condition_node)),
            label_ast="AST",
        )

    if update_node:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(update_node)),
            label_ast="AST",
        )

    if body_node:
        args.syntax_graph.nodes[args.n_id]["block_id"] = body_node
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(body_node)),
            label_ast="AST",
        )

    return args.n_id
