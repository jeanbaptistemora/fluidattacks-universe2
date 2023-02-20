from collections.abc import (
    Iterator,
)
from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
)
from utils.graph import (
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    param_node = graph.nodes[args.n_id]
    type_id = param_node["label_field_type"]
    identifier_id = param_node["label_field_name"]

    var_type = node_to_str(graph, type_id)
    var_name = node_to_str(graph, identifier_id)

    c_ids = match_ast_group_d(graph, args.n_id, "modifiers")

    return build_parameter_node(
        args, var_name, var_type, None, cast(Iterator[str], c_ids)
    )
