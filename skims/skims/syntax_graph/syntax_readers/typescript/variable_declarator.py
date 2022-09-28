# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declarator import (
    build_variable_declarator_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:

    childs_id = adj_ast(args.ast_graph, args.n_id)

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] == "type_annotation"
    ]

    variable_name = node_to_str(
        args.ast_graph, args.ast_graph.nodes[args.n_id]["label_field_name"]
    )

    value_id = args.ast_graph.nodes[args.n_id].get("label_field_value")

    return build_variable_declarator_node(
        args, valid_childs, variable_name, value_id
    )
