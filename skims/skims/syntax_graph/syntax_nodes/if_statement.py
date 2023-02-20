from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_if_node(
    args: SyntaxGraphArgs,
    condition_id: NId,
    true_id: NId | None,
    false_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        condition_id=condition_id,
        label_type="If",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(condition_id)),
        label_ast="AST",
    )

    if true_id:
        args.syntax_graph.nodes[args.n_id]["true_id"] = true_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(true_id)),
            label_ast="AST",
        )

    if false_id:
        args.syntax_graph.nodes[args.n_id]["false_id"] = false_id

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(false_id)),
            label_ast="AST",
        )

    return args.n_id
