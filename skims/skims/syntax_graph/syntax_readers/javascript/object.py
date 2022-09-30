# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.object import (
    build_object_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    valid_parameters = {
        "method_definition",
        "pair",
        "shorthand_property_identifier",
        "shorthand_property_identifier_pattern",
        "spread_element",
    }
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    return build_object_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] in valid_parameters
        ),
    )
