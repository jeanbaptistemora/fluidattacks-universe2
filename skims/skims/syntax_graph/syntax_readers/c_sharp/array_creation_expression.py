# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array_creation_expression import (
    build_array_creation_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(
        args.ast_graph, args.n_id, "array_type", "initializer_expression"
    )
    arr_type = children.get("array_type")
    arr_init = children.get("initializer_expression")
    return build_array_creation_expression_node(args, arr_type, arr_init)
