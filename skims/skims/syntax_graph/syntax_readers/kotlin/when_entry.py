from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    value_id = graph.nodes[args.n_id].get("label_field_conditions")
    if value_id:
        case_value = node_to_str(graph, value_id)
    else:
        case_value = "Default"

    execution_id = [graph.nodes[args.n_id]["label_field_body"]]

    return build_switch_section_node(args, case_value, execution_id)
