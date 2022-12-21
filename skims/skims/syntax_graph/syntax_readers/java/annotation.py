from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.annotation import (
    build_annotation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    annotation_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    annotation_name = node_to_str(args.ast_graph, annotation_id)
    args_id = args.ast_graph.nodes[args.n_id].get("label_field_arguments")

    return build_annotation_node(args, annotation_name, args_id)
