# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_case import (
    build_switch_case_node,
)
from syntax_graph.syntax_nodes.switch_default import (
    build_switch_default_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    case = match_ast_d(args.ast_graph, args.n_id, "case")

    if case:
        expr = node_to_str(args.ast_graph, args.n_id)
        return build_switch_case_node(args, None, expr)

    return build_switch_default_node(args, None)
