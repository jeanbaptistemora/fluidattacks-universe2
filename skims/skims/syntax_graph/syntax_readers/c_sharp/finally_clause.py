# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.finally_clause import (
    build_finally_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs = match_ast(args.ast_graph, args.n_id, "block")
    finally_block = childs.get("block")

    return build_finally_clause_node(args, finally_block)
