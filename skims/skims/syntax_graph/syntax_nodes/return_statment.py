from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_return_node(args: SyntaxGraphArgs, value_id: NId) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value_id=value_id,
        label_type="Return",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(value_id)),
        label_ast="AST",
    )

    return args.n_id
