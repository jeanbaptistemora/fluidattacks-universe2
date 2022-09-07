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


def build_while_statement_node(
    args: SyntaxGraphArgs, block: str, conditional: Optional[str]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        conditional_id=conditional,
        label_type="WhileStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block)),
        label_ast="AST",
    )

    if conditional:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(conditional)),
            label_ast="AST",
        )

    return args.n_id
