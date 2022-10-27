# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    condition_id = args.ast_graph.nodes[args.n_id]["label_field_condition"]
    if (
        args.ast_graph.nodes[condition_id]["label_type"]
        == "parenthesized_expression"
    ):
        condition_id = match_ast(args.ast_graph, condition_id).get("__1__")
    true_id = args.ast_graph.nodes[args.n_id]["label_field_consequence"]
    false_id = args.ast_graph.nodes[args.n_id].get("label_field_alternative")
    return build_if_node(args, condition_id, true_id, false_id)
