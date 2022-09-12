# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_each_statement import (
    build_for_each_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node = args.ast_graph.nodes[args.n_id]
    var_node = node.get("label_field_left")
    iterable_item = node.get("label_field_right")
    block_id = node.get("label_field_body")

    if not (var_node and iterable_item and block_id):
        raise MissingCaseHandling(f"Bad for statement handling in {args.n_id}")

    return build_for_each_statement_node(
        args, var_node, iterable_item, block_id
    )
