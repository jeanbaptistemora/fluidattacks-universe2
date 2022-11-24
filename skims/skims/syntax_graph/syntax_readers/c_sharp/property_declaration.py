from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.property_declaration import (
    build_property_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node = args.ast_graph.nodes[args.n_id]
    match_type = node["label_field_type"]
    match_identifier = node["label_field_name"]

    var_type = args.ast_graph.nodes[match_type].get("label_text")
    identifier = args.ast_graph.nodes[match_identifier].get("label_text")

    accessors = g.get_ast_childs(
        args.ast_graph, args.n_id, "accessor_declaration", depth=2
    )

    return build_property_declaration_node(
        args, var_type, identifier, list(accessors)
    )
