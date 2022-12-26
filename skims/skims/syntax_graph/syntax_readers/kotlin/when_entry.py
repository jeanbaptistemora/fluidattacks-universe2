from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
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

    body_id = graph.nodes[args.n_id].get("label_field_body")
    if not body_id:
        raise MissingCaseHandling(f"Bad when entry handling in {args.n_id}")

    return build_switch_section_node(args, case_value, [body_id])
