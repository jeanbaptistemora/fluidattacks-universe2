# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.else_clause import (
    build_else_clause_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "else")

    if len(match) == 2 and match["else"]:
        else_child = str(match["__0__"])
        return build_else_clause_node(args, else_child)

    raise MissingCaseHandling(f"Bad else handling in {args.n_id}")
