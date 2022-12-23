from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_each_statement import (
    build_for_each_statement_node,
)
from syntax_graph.syntax_nodes.for_statement import (
    build_for_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    body_id = n_attrs["label_field_control_structure_body"]
    var_node = n_attrs.get("label_field_variable_declaration")
    class_childs = list(adj_ast(graph, args.n_id))
    in_node = match_ast_d(graph, args.n_id, "in")

    if in_node and var_node:
        iterable_item = class_childs[class_childs.index(in_node) + 1]
        return build_for_each_statement_node(
            args, var_node, iterable_item, body_id
        )

    return build_for_statement_node(args, var_node, None, None, body_id)
