# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShardMetadataLanguage,
    NId,
)
from syntax_graph.constants import (
    C_SHARP_EXPRESSION,
    C_SHARP_STATEMENT,
)
from syntax_graph.syntax_nodes.do_statement import (
    build_do_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:

    graph = args.ast_graph

    c_ids = adj_ast(args.ast_graph, args.n_id)

    if args.language == GraphShardMetadataLanguage.CSHARP:
        body_id = [
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] in C_SHARP_STATEMENT
        ].pop()
        condition_node = [
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] in C_SHARP_EXPRESSION
        ].pop()
    else:
        body_id = args.ast_graph.nodes[args.n_id]["label_field_body"]
        condition_node = args.ast_graph.nodes[args.n_id][
            "label_field_condition"
        ]

    return build_do_statement_node(args, body_id, condition_node)
