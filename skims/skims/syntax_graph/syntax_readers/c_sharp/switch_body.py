# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_body import (
    build_switch_body_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    case_ids = match_ast_group_d(graph, args.n_id, "switch_section")
    return build_switch_body_node(args, case_ids, None)
