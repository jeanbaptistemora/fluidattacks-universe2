# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.member_binding_expression import (
    build_member_binding_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    field_node = args.ast_graph.nodes[args.n_id]["label_field_name"]
    return build_member_binding_expression_node(args, field_node)
