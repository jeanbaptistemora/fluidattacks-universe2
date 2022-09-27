# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.catch_clause import (
    build_catch_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    block = args.ast_graph.nodes[args.n_id]["label_field_body"]
    childs = match_ast(args.ast_graph, args.n_id, "catch_formal_parameter")
    c_param = childs.get("catch_formal_parameter")
    return build_catch_clause_node(args, block, None, None, c_param)
