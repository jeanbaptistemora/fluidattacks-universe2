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


def build_member_access_node(
    args: SyntaxGraphArgs,
    member: str,
    expression: str,
    expression_id: NId,
    member_id: Optional[NId] = None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        member=member,
        expression=expression,
        expression_id=expression_id,
        label_type="MemberAccess",
    )

    if member_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(member_id)),
            label_ast="AST",
        )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression_id)),
        label_ast="AST",
    )

    return args.n_id
