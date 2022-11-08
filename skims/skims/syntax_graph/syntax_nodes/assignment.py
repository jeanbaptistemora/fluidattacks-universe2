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


def build_assignment_node(
    args: SyntaxGraphArgs, var_id: NId, val_id: NId, operator: Optional[str]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable_id=var_id,
        value_id=val_id,
        label_type="Assignment",
    )

    if operator:
        args.syntax_graph.nodes[args.n_id]["operator"] = operator

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(val_id)),
        label_ast="AST",
    )

    return args.n_id
