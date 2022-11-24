from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    JAVASCRIPT_STATEMENT,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
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
    value_id = graph.nodes[args.n_id].get("label_field_value")
    if value_id:
        case_value = node_to_str(graph, value_id)
    else:
        case_value = "Default"

    execution_ids = [
        _id
        for _id in adj_ast(graph, args.n_id)
        if graph.nodes[_id]["label_type"] in JAVASCRIPT_STATEMENT
        and graph.nodes[_id]["label_type"] != "break_statement"
    ]

    return build_switch_section_node(args, case_value, execution_ids)
