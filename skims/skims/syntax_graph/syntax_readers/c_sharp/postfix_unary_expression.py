# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.postfix_unary_expression import (
    build_postfix_unary_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_expression = match_ast(args.ast_graph, args.n_id)
    var_node = str(match_expression["__0__"])
    operator = args.ast_graph.nodes[match_expression["__1__"]]["label_text"]
    return build_postfix_unary_expression_node(args, operator, var_node)
