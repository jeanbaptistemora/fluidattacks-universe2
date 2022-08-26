from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_array_access_node(
    args: SyntaxGraphArgs,
    index: str,
    array_id: str,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        access_index=index,
        label_type="ArrayAccess",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(array_id)),
        label_ast="AST",
    )

    return args.n_id
