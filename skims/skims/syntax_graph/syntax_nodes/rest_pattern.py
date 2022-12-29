from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_rest_pattern_node(args: SyntaxGraphArgs, identifier_id: NId) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="RestPattern",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(identifier_id)),
        label_ast="AST",
    )

    return args.n_id
