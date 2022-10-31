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


def build_for_statement_node(
    args: SyntaxGraphArgs,
    initializer_node: Optional[NId],
    condition_node: Optional[NId],
    update_node: Optional[NId],
    body_node: NId,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        block_id=body_node,
        label_type="ForStatement",
    )

    if initializer_node:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(initializer_node)),
            label_ast="AST",
        )

    if condition_node:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(condition_node)),
            label_ast="AST",
        )

    if update_node:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(update_node)),
            label_ast="AST",
        )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(body_node)),
        label_ast="AST",
    )

    return args.n_id
