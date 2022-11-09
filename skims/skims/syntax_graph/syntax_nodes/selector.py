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
    Iterator,
    Optional,
)


def build_selector_node(
    args: SyntaxGraphArgs,
    identifier: Optional[str],
    c_ids: Optional[Iterator[NId]],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Selector",
    )

    if identifier:
        args.syntax_graph.nodes[args.n_id]["selector_name"] = identifier

    if c_ids:
        for c_id in c_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(c_id)),
                label_ast="AST",
            )

    return args.n_id
