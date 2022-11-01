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


def build_switch_default_node(
    args: SyntaxGraphArgs, body_id: Optional[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="SwitchDefault",
    )

    if body_id:
        args.syntax_graph.nodes[args.n_id]["block_id"] = body_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(body_id)),
            label_ast="AST",
        )

    return args.n_id
