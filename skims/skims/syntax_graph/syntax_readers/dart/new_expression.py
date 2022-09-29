# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.new_expression import (
    build_new_expression_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(args.ast_graph, args.n_id)

    if (const_id := match_childs.get("__1__")) and (
        args_id := match_childs.get("__2__")
    ):
        return build_new_expression_node(args, const_id, args_id)
    raise MissingCaseHandling(f"Bad new expression handling in {args.n_id}")
