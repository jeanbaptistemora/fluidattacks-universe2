from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.extension_declaration import (
    build_extension_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    extension_name = (
        node_to_str(args.ast_graph, name_id)
        if (name_id := as_attrs.get("label_field_name"))
        else None
    )
    class_id = as_attrs["label_field_class"]
    body_id = as_attrs["label_field_body"]

    return build_extension_declaration_node(
        args, class_id, body_id, extension_name
    )
