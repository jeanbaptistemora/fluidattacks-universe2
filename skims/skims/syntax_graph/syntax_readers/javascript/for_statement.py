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
    MissingCaseHandling,
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node = args.ast_graph.nodes[args.n_id]
    body_node = node.get("label_field_body")
    initializer_node = node.get("label_field_initializer") or node.get(
        "label_field_left"
    )
    condition_node = node.get("label_field_condition") or node.get(
        "label_field_right"
    )

    if not (initializer_node and condition_node and body_node):
        raise MissingCaseHandling(f"Bad for statement handling in {args.n_id}")

    increment_node = node.get("label_field_increment")
    return build_for_statement_node(
        args, initializer_node, condition_node, increment_node, body_node
    )
