# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_switch_case_node(
    args: SyntaxGraphArgs,
    expression: Optional[NId],
    value: str,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        label_type="SwitchCase",
    )

    if expression:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(expression)),
            label_ast="AST",
        )

    return args.n_id
