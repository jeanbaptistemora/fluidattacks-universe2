# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_this_expression_node(
    args: SyntaxGraphArgs,
    expression: str,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression_id=expression,
        label_type="ThisExpression",
    )
    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression)),
        label_ast="AST",
    )

    return args.n_id
