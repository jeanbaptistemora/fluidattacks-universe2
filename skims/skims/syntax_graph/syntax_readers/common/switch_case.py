from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_case import (
    build_switch_case_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    value_id = args.ast_graph.nodes[args.n_id]["label_field_value"]
    case_value = node_to_str(args.ast_graph, value_id)
    expression = match_ast_d(args.ast_graph, args.n_id, "expression_statement")
    if not expression:
        raise MissingCaseHandling(f"Bad switch case handling in {args.n_id}")

    return build_switch_case_node(args, expression, case_value)
