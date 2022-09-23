# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignable_selector import (
    build_assignable_selector_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    c_ids = [
        child
        for child in adj_ast(graph, args.n_id)
        if args.ast_graph.nodes[child]["label_type"]
        in {"identifier", "index_selector"}
    ]

    return build_assignable_selector_node(args, iter(c_ids))
