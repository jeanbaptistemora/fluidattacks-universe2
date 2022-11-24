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
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attr = graph.nodes[args.n_id]
    var_id = n_attr["label_field_left"]
    val_id = n_attr["label_field_right"]
    op_id = n_attr.get("label_field_operator")
    operator = str(graph.nodes[op_id]["label_text"])
    if (
        graph.nodes[var_id]["label_type"] == "assignable_expression"
        and len(adj_ast(graph, var_id)) == 1
    ):
        var_id = match_ast(graph, var_id).get("__0__")

    return build_assignment_node(args, var_id, val_id, operator)
