# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.ternary_operation import (
    build_ternary_operation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    cond_id = n_attrs["label_field_condition"]
    alt_id = n_attrs["label_field_alternative"]
    cons_id = n_attrs["label_field_consequence"]
    return build_ternary_operation_node(args, cond_id, alt_id, cons_id)
