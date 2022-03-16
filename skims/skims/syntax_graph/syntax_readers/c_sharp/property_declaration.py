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
    match_type = g.match_ast(args.ast_graph, args.n_id, "predefined_type")
    match_identifier = g.match_ast(args.ast_graph, args.n_id, "identifier")
    var_type = args.ast_graph.nodes[match_type["predefined_type"]][
        "label_text"
    ]
    identifier = args.ast_graph.nodes[match_identifier["identifier"]][
        "label_text"
    ]
    accessors = g.get_ast_childs(
        args.ast_graph, args.n_id, "accessor_declaration", depth=2
    )

    return build_property_declaration_node(
        args, var_type, identifier, list(accessors)
    )
