# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
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

    node_types = {
        "array_initializer",
        "call_expression",
        "cast_expression",
        "decimal_integer_literal",
        "identifier",
        "number",
        "object",
        "string",
        "string_literal",
    }

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] in node_types
    ]

    if len(childs_id) > 2 and not valid_childs:
        raise MissingCaseHandling(f"Bad array handling in {args.n_id}")

    return build_array_node(args, valid_childs)
