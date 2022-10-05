# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_unary_expression_node(
    args: SyntaxGraphArgs,
    operator: str,
    operand_id: NId,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        operator=operator,
        operand_id=operand_id,
        label_type="UnaryExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(operand_id)),
        label_ast="AST",
    )

    return args.n_id
