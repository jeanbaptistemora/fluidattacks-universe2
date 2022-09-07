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


def build_resource_node(
    args: SyntaxGraphArgs,
    variable: str,
    variable_type: Optional[str],
    value: Optional[str],
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        variable=variable,
        variable_type=variable_type,
        value_id=value,
        label_type="Resource",
    )

    if value:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(value)),
            label_ast="AST",
        )

    return args.n_id
