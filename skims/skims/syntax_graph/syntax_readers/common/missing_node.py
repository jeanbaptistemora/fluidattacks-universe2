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
    match_ast,
)


def reader(args: SyntaxGraphArgs, n_type: str) -> NId:
    graph = args.ast_graph
    c_ids = list(filter(None, match_ast(graph, args.n_id).values()))

    return build_missing_node(
        args,
        n_type,
        c_ids,
    )
