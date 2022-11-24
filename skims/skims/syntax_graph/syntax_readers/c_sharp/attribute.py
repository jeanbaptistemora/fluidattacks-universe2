from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.attribute import (
    build_attribute_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    arg_list = match_ast_d(
        args.ast_graph, args.n_id, "attribute_argument_list"
    )

    attr_name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    attr_name = args.ast_graph.nodes[attr_name_id].get("label_text")

    return build_attribute_node(args, attr_name, arg_list)
