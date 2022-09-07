# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.new_expression import (
    build_new_expression_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node = args.ast_graph.nodes[args.n_id]
    index_id = node.get("label_field_index")
    object_id = node.get("label_field_object")

    if not object_id:
        raise MissingCaseHandling(f"Bad subscript expression in {args.n_id}")

    return build_new_expression_node(args, object_id, index_id)
