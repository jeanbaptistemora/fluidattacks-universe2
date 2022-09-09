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
)


def build_getter_signature_node(
    args: SyntaxGraphArgs, name: str, c_ids: Iterator[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="GetterSignature",
        label_name=name,
    )

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
