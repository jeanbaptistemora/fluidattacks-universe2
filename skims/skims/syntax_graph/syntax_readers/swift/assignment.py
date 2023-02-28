from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
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


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    as_attrs = args.ast_graph.nodes[args.n_id]
    var_id = as_attrs["label_field_target"]
    if (
        graph.nodes[var_id]["label_type"] == "directly_assignable_expression"
        and (childs := adj_ast(graph, var_id))
        and len(childs) == 1
    ):
        var_id = childs[0]
    val_id = as_attrs.get("label_field_result")
    operator = as_attrs.get("label_field_operator")
    operator = node_to_str(graph, operator)
    return build_assignment_node(args, var_id, val_id, operator)
