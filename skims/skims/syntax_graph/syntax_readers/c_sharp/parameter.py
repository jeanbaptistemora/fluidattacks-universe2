# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    param_node = graph.nodes[args.n_id]

    identifier_id = param_node["label_field_name"]
    var_name = node_to_str(graph, identifier_id)

    type_id = param_node.get("label_field_type")
    var_type = node_to_str(graph, type_id) if type_id else None

    def_value = None
    equals_clause = match_ast_d(graph, args.n_id, "equals_value_clause")
    if equals_clause:
        def_value = match_ast(graph, equals_clause, "=").get("__0__")

    return build_parameter_node(args, var_name, var_type, def_value)
