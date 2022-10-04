# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    C_SHARP_EXPRESSION,
)
from syntax_graph.syntax_nodes.argument import (
    build_argument_node,
)
from syntax_graph.syntax_nodes.named_argument import (
    build_named_argument_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    first_child, *other_childs = adj_ast(args.ast_graph, args.n_id)

    if not other_childs:
        return args.generic(args.fork_n_id(first_child))

    match = match_ast(args.ast_graph, args.n_id, "name_colon")
    if name_colon := match.get("name_colon"):
        var_id = match_ast_d(args.ast_graph, name_colon, "identifier")
        return build_named_argument_node(
            args, str(var_id), val_id=str(match["__0__"])
        )

    if valid_childs := [
        _id
        for _id in adj_ast(args.ast_graph, args.n_id)
        if args.ast_graph.nodes[_id]["label_type"]
        in C_SHARP_EXPRESSION.union({"declaration_expression"})
    ]:
        return build_argument_node(args, iter(valid_childs))

    raise MissingCaseHandling(f"Bad argument handling in {args.n_id}")
