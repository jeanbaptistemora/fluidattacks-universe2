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
    var_node = args.ast_graph.nodes[args.n_id]["label_field_left"]
    iterable_item = args.ast_graph.nodes[args.n_id]["label_field_right"]
    block = args.ast_graph.nodes[args.n_id]["label_field_body"]
    return build_for_each_statement_node(args, var_node, iterable_item, block)
