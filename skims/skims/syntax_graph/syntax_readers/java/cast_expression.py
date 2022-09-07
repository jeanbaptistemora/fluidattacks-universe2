# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.cast_expression import (
    build_cast_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    type_id = as_attrs["label_field_type"]
    val_id = as_attrs["label_field_value"]

    return build_cast_expression_node(
        args,
        type_id,
        val_id,
    )
