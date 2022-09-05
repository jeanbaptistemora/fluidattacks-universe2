from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_case import (
    build_switch_case_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    value_id = args.ast_graph.nodes[args.n_id]["label_field_value"]
    case_value = node_to_str(args.ast_graph, value_id)
    childs = match_ast(args.ast_graph, args.n_id, "expression_statement")
    expression = childs.get("expression_statement")

    return build_switch_case_node(args, expression, case_value)
