# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.while_statement import (
    build_while_statement_node,
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
    if graph.nodes[body_id]["label_type"] == "expression_statement":
        body_id = match_ast(graph, body_id)["__0__"]
    if graph.nodes[body_id]["label_type"] == "parenthesized_expression":
        body_id = match_ast(graph, body_id)["__1__"]

    cond_id = n_attrs["label_field_condition"]
    if graph.nodes[cond_id]["label_type"] == "parenthesized_expression":
        cond_id = match_ast(graph, cond_id)["__1__"]

    return build_while_statement_node(args, body_id, cond_id)
