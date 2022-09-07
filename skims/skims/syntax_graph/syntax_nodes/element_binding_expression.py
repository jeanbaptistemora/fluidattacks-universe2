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
    List,
)


def build_element_binding_expression_node(
    args: SyntaxGraphArgs,
    childs: List[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="ElementBindingExpression",
    )
    for nid in childs:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(nid)),
            label_ast="AST",
        )

    return args.n_id
