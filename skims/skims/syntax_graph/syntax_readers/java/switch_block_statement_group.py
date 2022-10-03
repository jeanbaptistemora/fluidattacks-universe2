# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    JAVA_STATEMENT,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs = [
        _id
        for _id in adj_ast(graph, args.n_id)
        if graph.nodes[_id]["label_type"] in JAVA_STATEMENT
    ]

    if len(childs) >= 1:
        body_id = childs[0]
    else:
        body_id = None

    case_id = match_ast_d(graph, args.n_id, "switch_label")
    c_ids = filter(None, (body_id, case_id))

    return build_switch_section_node(args, c_ids)
