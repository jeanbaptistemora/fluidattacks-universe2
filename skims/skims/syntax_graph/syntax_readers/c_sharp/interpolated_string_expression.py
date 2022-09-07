# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.interpolated_string_expression import (
    build_interpolated_string_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = [
        c_id
        for c_id in adj_ast(args.ast_graph, args.n_id)
        if args.ast_graph.nodes[c_id].get("label_type") == "interpolation"
    ]
    return build_interpolated_string_expression_node(args, c_ids)
