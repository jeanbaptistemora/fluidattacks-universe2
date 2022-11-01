# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_case import (
    build_switch_case_node,
)
from syntax_graph.types import (
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
    value_id = graph.nodes[args.n_id]["label_field_value"]
    case_value = node_to_str(graph, value_id)
    childs = match_ast(graph, args.n_id, "case", ":", "break_statement")
    expr_id = childs.get("__1__")
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
    return build_switch_case_node(args, expr_id, case_value)
