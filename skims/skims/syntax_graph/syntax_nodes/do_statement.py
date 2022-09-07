# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_do_statement_node(
    args: SyntaxGraphArgs, block: str, conditional: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block,
        conditional_id=conditional,
        label_type="DoStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(conditional)),
        label_ast="AST",
    )

    return args.n_id
