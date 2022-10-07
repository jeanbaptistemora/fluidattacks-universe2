# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.initializer_expression import (
    build_initializer_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs_id = adj_ast(
        args.ast_graph,
        args.n_id,
    )

    node_types = {"[", "]", ":"}

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] not in node_types
    ]

    return build_initializer_expression_node(args, iter(valid_childs))
