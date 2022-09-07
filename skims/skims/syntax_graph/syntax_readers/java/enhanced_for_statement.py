# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.enhanced_for_statement import (
    build_enhanced_for_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_id = args.ast_graph.nodes[args.n_id]
    body_node = node_id["label_field_body"]
    value_node = node_id["label_field_body"]
    type_str = args.ast_graph.nodes[node_id["label_field_type"]]["label_text"]
    name_str = args.ast_graph.nodes[node_id["label_field_name"]]["label_text"]
    return build_enhanced_for_statement_node(
        args, type_str, name_str, value_node, body_node
    )
