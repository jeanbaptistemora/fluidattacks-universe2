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


def build_array_creation_expression_node(
    args: SyntaxGraphArgs,
    type_id: Optional[NId],
    initializer_id: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        array_type_id=type_id,
        initializer_id=initializer_id,
        label_type="ArrayCreation",
    )

    if type_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(type_id)),
            label_ast="AST",
        )

    if initializer_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(initializer_id)),
            label_ast="AST",
        )

    return args.n_id
