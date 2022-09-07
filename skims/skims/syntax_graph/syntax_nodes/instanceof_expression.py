# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_instanceof_expression_node(
    args: SyntaxGraphArgs,
    left_id: NId,
    right_id: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        left_id=left_id,
        right_id=right_id,
        label_type="InstanceOfExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(left_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(right_id)),
        label_ast="AST",
    )

    return args.n_id
