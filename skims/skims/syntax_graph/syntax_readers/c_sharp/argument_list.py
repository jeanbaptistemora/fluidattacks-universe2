# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.argument_list import (
    build_argument_list_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = match_ast_group_d(
        args.ast_graph, args.n_id, "argument"
    ) or match_ast_group_d(args.ast_graph, args.n_id, "attribute_argument")
    return build_argument_list_node(args, iter(c_ids))
