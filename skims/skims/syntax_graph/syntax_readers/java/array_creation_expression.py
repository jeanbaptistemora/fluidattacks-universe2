# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array_creation_expression import (
    build_array_creation_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attr = args.ast_graph.nodes[args.n_id]
    type_id = n_attr["label_field_type"]
    arr_type = node_to_str(args.ast_graph, type_id)

    arr_value = n_attr.get("label_field_value")

    return build_array_creation_expression_node(args, arr_type, arr_value)
