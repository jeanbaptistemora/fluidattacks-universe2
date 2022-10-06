# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    var_name = node_to_str(args.ast_graph, n_attrs["label_field_name"])
    val_id = n_attrs["label_field_value"]

    if args.ast_graph.nodes[val_id]["label_type"] == "conditional_type":
        val_id = args.ast_graph.nodes[val_id]["label_field_consequence"]

    return build_variable_declaration_node(args, var_name, None, val_id)
