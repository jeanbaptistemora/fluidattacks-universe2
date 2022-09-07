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
    Iterable,
)


def build_catch_declaration_node(
    args: SyntaxGraphArgs, c_ids: Iterable[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="CatchDeclaration",
    )

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
