# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_switch_expression_node(
    args: SyntaxGraphArgs,
    body_id: NId,
    condition_id: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        body_id=body_id,
        value_id=condition_id,
        label_type="SwitchExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(body_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(condition_id)),
        label_ast="AST",
    )

    return args.n_id
