# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_statement import (
    build_for_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    body_id = n_attrs["label_field_body"]
    initializer_id = n_attrs["label_field_initializer"]
    condition_id = n_attrs["label_field_condition"]

    if graph.nodes[body_id]["label_type"] == "expression_statement":
        body_id = match_ast(graph, body_id)["__0__"]

    if graph.nodes[body_id]["label_type"] == "parenthesized_expression":
        body_id = match_ast(graph, body_id)["__1__"]

    increment_id = n_attrs.get("label_field_increment")
    return build_for_statement_node(
        args, initializer_id, condition_id, increment_id, body_id
    )
