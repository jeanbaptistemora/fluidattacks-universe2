# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_element_value_pair_node(
    args: SyntaxGraphArgs, element_id: NId, val_id: NId
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        element_id=element_id,
        value_id=val_id,
        label_type="ElementValuePair",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(element_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(val_id)),
        label_ast="AST",
    )

    return args.n_id
