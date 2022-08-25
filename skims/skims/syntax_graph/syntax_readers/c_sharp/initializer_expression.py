from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.initializer_expression import (
    build_initializer_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = match_ast_group_d(graph, args.n_id, "assignment_expression")

    if len(c_ids) == 0:
        children = adj_ast(graph, args.n_id)
        ignore_types = ["{", "}", ","]
        c_ids = [
            id
            for id in children
            if graph.nodes[id]["label_type"] not in ignore_types
        ]

    return build_initializer_expression_node(args, iter(c_ids))
