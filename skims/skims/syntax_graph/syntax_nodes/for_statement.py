from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_for_statement_node(
    args: SyntaxGraphArgs,
    initializer_node: str,
    condition_node: str,
    update_node: str,
    body_node: str,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        label_type="ForStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(initializer_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(condition_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(update_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(body_node)),
        label_ast="AST",
    )

    return args.n_id
