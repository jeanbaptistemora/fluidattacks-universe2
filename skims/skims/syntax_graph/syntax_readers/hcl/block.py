from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.object import (
    build_object_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    valid_parameters = {
        "attribute",
        "block",
    }
    graph = args.ast_graph

    name_id = match_ast_d(graph, args.n_id, "string_lit")
    name = ""
    if name_id:
        name = node_to_str(graph, str(name_id))[1:-1]
    else:
        name_id = match_ast_d(graph, args.n_id, "identifier")
        name = node_to_str(graph, str(name_id))

    body_id = match_ast_d(graph, args.n_id, "body")

    c_ids = adj_ast(graph, str(body_id))

    return build_object_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] in valid_parameters
        ),
        name=name,
    )
