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
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    valid_parameters = {"class_body"}
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    name = ""
    for child in c_ids:
        if graph.nodes[child]["label_type"] == "delegation_specifier":
            name = node_to_str(graph, child)
    return build_object_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] in valid_parameters
        ),
        name=name,
    )
