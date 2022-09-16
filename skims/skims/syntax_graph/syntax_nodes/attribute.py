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


def build_attribute_node(
    args: SyntaxGraphArgs,
    attr_name: str,
    attr_list: Optional[str],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=attr_name,
        label_type="Attribute",
    )

    if attr_list:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(attr_list)),
            label_ast="AST",
        )

    return args.n_id
