# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_default import (
    build_switch_default_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)

    if len(c_ids) < 3:
        expr_id = None
    else:
        expr_id = c_ids[2]

    if (
        expr_id
        and graph.nodes[expr_id]["label_type"] == "expression_statement"
    ):
        expr_id = match_ast(graph, expr_id).get("__0__")

    if (
        expr_id
        and graph.nodes[expr_id]["label_type"] == "parenthesized_expression"
    ):
        expr_id = match_ast(graph, expr_id)["__1__"]

    return build_switch_default_node(args, expr_id)
