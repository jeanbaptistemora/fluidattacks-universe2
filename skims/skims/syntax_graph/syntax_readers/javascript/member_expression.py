from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.member_access import (
    build_member_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    member_id = args.ast_graph.nodes[args.n_id]["label_field_object"]
    member = node_to_str(args.ast_graph, member_id)
    memb_type = args.ast_graph.nodes[args.n_id]["label_type"]
    if memb_type not in {"member_expression", "call_expression"}:
        member_id = None

    expression_id = args.ast_graph.nodes[args.n_id]["label_field_property"]
    expression = node_to_str(args.ast_graph, expression_id)

    return build_member_access_node(
        args, member, expression, expression_id, member_id
    )
