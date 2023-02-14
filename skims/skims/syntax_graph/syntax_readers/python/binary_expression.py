from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.binary_operation import (
    build_binary_operation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    operator_id = n_attrs.get("label_field_operators") or n_attrs.get(
        "label_field_operator"
    )
    operator = graph.nodes[operator_id]["label_text"]
    childs = adj_ast(graph, args.n_id)
    return build_binary_operation_node(args, operator, childs[0], childs[-1])
