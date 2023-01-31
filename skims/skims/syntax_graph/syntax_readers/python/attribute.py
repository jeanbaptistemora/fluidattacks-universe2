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
    attr_id = args.ast_graph.nodes[args.n_id]["label_field_attribute"]
    obj_id = args.ast_graph.nodes[args.n_id]["label_field_object"]
    member = node_to_str(args.ast_graph, attr_id)
    expression = node_to_str(args.ast_graph, obj_id)
    return build_member_access_node(args, member, expression, obj_id)
