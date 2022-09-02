from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.catch_parameter import (
    build_catch_parameter_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
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
    cp_node = graph.nodes[args.n_id]
    identifier_id = cp_node["label_field_name"]
    identifier = node_to_str(graph, identifier_id)

    childs = match_ast(graph, args.n_id, "catch_type")
    if catch_type := childs.get("catch_type"):
        return build_catch_parameter_node(args, identifier, catch_type)

    raise MissingCaseHandling(f"Bad catch parameter handling in {args.n_id}")
