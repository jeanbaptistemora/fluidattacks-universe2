# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node = args.ast_graph.nodes[args.n_id]
    value_id = node.get("label_field_value")

    if not value_id:
        raise MissingCaseHandling(
            f"Bad export statement handling in {args.n_id}"
        )
    expr = node_to_str(args.ast_graph, value_id)

    args.syntax_graph.add_node(
        args.n_id,
        expression=expr,
        label_type="Export",
    )

    return args.n_id
