from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.missing_node import (
    build_missing_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs, n_type: str) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)

    return build_missing_node(
        args,
        n_type,
        iter(c_ids),
    )
