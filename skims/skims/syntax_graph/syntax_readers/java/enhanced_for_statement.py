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
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_id = args.ast_graph.nodes[args.n_id]
    var_node = node_id["label_field_name"]
    iterable_item = node_id["label_field_value"]
    block = node_id["label_field_body"]

    return build_for_each_statement_node(args, var_node, iterable_item, block)
