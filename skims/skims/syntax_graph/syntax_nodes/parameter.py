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


def build_parameter_node(
    args: SyntaxGraphArgs,
    variable: Optional[str],
    variable_type: Optional[str],
    modifier: Optional[str],
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        label_type="Parameter",
    )

    if variable:
        args.syntax_graph.nodes[args.n_id]["variable"] = variable

    if variable_type:
        args.syntax_graph.nodes[args.n_id]["variable_type"] = variable_type

    if modifier:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(modifier)),
            label_ast="AST",
        )

    return args.n_id
