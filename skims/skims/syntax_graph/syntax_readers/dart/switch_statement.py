# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_statement import (
    build_switch_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    body_id = graph.nodes[args.n_id]["label_field_body"]
    value_id = graph.nodes[args.n_id]["label_field_condition"]
    if graph.nodes[value_id]["label_type"] == "parenthesized_expression":
        value_id = match_ast(graph, value_id).get("__1__")
    return build_switch_statement_node(args, body_id, value_id)
