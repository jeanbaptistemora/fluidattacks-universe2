# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    param_identifier = match_ast_d(graph, args.n_id, "identifier")
    param_name = None
    if param_identifier:
        param_name = node_to_str(graph, param_identifier)

    c_ids = adj_ast(graph, args.n_id)
    invalid_childs = {"this", ".", "?", ";"}
    return build_parameter_node(
        args,
        param_name,
        None,
        None,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] not in invalid_childs
        ),
    )
