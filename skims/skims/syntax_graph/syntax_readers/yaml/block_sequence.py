from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs_id = adj_ast(
        args.ast_graph,
        args.n_id,
    )

    invalid_types = {
        "[",
        "]",
        "{",
        "}",
        ",",
        ";",
    }

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] not in invalid_types
    ]

    usable_childs = []
    for child in valid_childs:
        curr_child = adj_ast(args.ast_graph, child)[1]
        if args.ast_graph.nodes[curr_child]["label_type"] != "block_node":
            usable_childs.append(curr_child)
        else:
            usable_childs.append(adj_ast(args.ast_graph, curr_child)[0])

    return build_array_node(args, usable_childs)
