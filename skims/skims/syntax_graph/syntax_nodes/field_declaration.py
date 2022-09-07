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


def build_field_declaration_node(
    args: SyntaxGraphArgs, vars_list: List[str], field_type: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        field_type=field_type,
        label_type="FieldDeclaration",
    )

    for var_id in vars_list:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(var_id)),
            label_ast="AST",
        )

    return args.n_id
