# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.element_access import (
    build_element_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    expression_id = args.ast_graph.nodes[args.n_id]["label_field_expression"]
    arguments_id = args.ast_graph.nodes[args.n_id]["label_field_subscript"]
    return build_element_access_node(args, expression_id, arguments_id)
