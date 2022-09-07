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


def build_finally_clause_node(
    args: SyntaxGraphArgs,
    block_node: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="FinallyClause",
    )

    if block_node:
        args.syntax_graph.nodes[args.n_id]["block_id"] = block_node
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_node)),
            label_ast="AST",
        )

    return args.n_id
