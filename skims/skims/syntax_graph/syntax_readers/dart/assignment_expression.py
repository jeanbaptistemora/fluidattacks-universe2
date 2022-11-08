# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attr = args.ast_graph.nodes[args.n_id]
    var_id = n_attr.get("label_field_left")

    if (
        not var_id
        and (c_ids := adj_ast(args.ast_graph, args.n_id))
        and len(c_ids) >= 3
    ):
        idx_operator = len(c_ids) // 2
        var_id = c_ids[idx_operator - 1]
        operator = node_to_str(args.ast_graph, c_ids[idx_operator])
        val_id = c_ids[-1]
    else:
        val_id = n_attr["label_field_right"]
        op_id = n_attr.get("label_field_operator")
        operator = str(args.ast_graph.nodes[op_id]["label_text"])

    if (
        var_id
        and args.ast_graph.nodes[var_id]["label_type"]
        == "assignable_expression"
    ):
        var_id = match_ast(args.ast_graph, var_id).get("__0__")

    return build_assignment_node(args, var_id, val_id, operator)
