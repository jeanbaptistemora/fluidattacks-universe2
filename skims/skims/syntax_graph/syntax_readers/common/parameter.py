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
    MissingCaseHandling,
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
    graph = args.ast_graph
    childs = adj_ast(graph, args.n_id)

    if len(childs) > 3:
        raise MissingCaseHandling(f"Bad parameter handling in {args.n_id}")

    parameter = graph.nodes[args.n_id]
    type_id = parameter.get("label_field_type")
    identifier_id = parameter["label_field_name"]

    variable = node_to_str(graph, identifier_id)
    variable_type = None if type_id is None else node_to_str(graph, type_id)
    modifiers_id = match_ast_d(graph, args.n_id, "modifiers")

    return build_parameter_node(args, variable, variable_type, modifiers_id)
