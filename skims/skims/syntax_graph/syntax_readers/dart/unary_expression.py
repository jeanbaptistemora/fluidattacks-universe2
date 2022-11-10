# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)
    ignored_types = {";"}
    filtered_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_types
    ]
    return build_expression_statement_node(args, iter(filtered_ids))
