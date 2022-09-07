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


def reader(args: SyntaxGraphArgs) -> NId:
    initializer_node = args.ast_graph.nodes[args.n_id]["label_field_init"]
    condition_node = args.ast_graph.nodes[args.n_id]["label_field_condition"]
    body_node = args.ast_graph.nodes[args.n_id]["label_field_body"]
    update_node = args.ast_graph.nodes[args.n_id]["label_field_update"]
    return build_for_statement_node(
        args, initializer_node, condition_node, update_node, body_node
    )
