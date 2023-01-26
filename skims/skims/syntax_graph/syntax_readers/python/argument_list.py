from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.argument_list import (
    build_argument_list_node,
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
        "(",
        ",",
        ")",
    }

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] not in invalid_types
    ]

    return build_argument_list_node(args, iter(valid_childs))
