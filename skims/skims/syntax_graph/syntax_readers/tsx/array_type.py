# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array_type import (
    build_array_type_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:

    childs_id = adj_ast(
        args.ast_graph,
        args.n_id,
    )

    c_id = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] == "predefined_type"
    ]

    array_type = node_to_str(args.ast_graph, c_id[0])

    return build_array_type_node(args, array_type)
