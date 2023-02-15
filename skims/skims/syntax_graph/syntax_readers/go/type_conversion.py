from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.type_conversion import (
    type_conversion_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)

invalid_types = {
    "[",
    "]",
    "{",
    "}",
    ",",
    ";",
    "(",
    ")",
}


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    value_id = n_attrs["label_field_operand"]
    value = node_to_str(args.ast_graph, value_id)
    type_id = n_attrs["label_field_type"]
    var_type = node_to_str(args.ast_graph, type_id)
    graph = args.ast_graph
    _, *c_ids, _ = adj_ast(graph, args.n_id)
    c_ids = [
        child
        for child in c_ids
        if args.ast_graph.nodes[child]["label_type"] not in invalid_types
    ]
    return type_conversion_node(args, value, var_type, iter(c_ids))
