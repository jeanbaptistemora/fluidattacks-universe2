# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.try_statement import (
    build_try_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    block_node = args.ast_graph.nodes[args.n_id]["label_field_body"]
    childs = match_ast(
        args.ast_graph,
        args.n_id,
        "catch_clause",
        "finally_clause",
        "resource_specification",
    )
    catch_blocks = match_ast_group_d(args.ast_graph, args.n_id, "catch_clause")
    try_block = childs.get("finally_clause")
    resources_espec = childs.get("resource_specification")

    return build_try_statement_node(
        args, block_node, catch_blocks, try_block, resources_espec
    )
