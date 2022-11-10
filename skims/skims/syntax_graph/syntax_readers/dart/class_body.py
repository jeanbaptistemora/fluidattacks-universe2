# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_body import (
    build_class_body_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    ignored_types = {";", "{", "}", "function_body"}
    filtered_ids = [
        _id
        for _id in c_ids
        if graph.nodes[_id]["label_type"] not in ignored_types
    ]
    return build_class_body_node(args, filtered_ids)
