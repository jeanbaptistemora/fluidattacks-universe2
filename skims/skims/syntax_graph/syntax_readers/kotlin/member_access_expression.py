from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.member_access import (
    build_member_access_node,
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
    graph = args.ast_graph
    member_id = graph.nodes[args.n_id]["label_field_navigation_suffix"]
    expression_id = graph.nodes[args.n_id]["label_field_expression"]

    if graph.nodes[member_id]["label_type"] == "navigation_suffix" and (
        identifier_id := match_ast(graph, member_id).get("__1__")
    ):
        member = node_to_str(graph, identifier_id)
    else:
        member = node_to_str(graph, member_id)

    expression = node_to_str(graph, expression_id)
    return build_member_access_node(args, member, expression, expression_id)
