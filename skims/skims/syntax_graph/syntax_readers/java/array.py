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

    node_types = {
        "array_initializer",
        "binary_expression",
        "cast_expression",
        "decimal_integer_literal",
        "identifier",
        "object",
        "string",
        "string_literal",
    }

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] in node_types
    ]

    return build_array_node(args, valid_childs)
