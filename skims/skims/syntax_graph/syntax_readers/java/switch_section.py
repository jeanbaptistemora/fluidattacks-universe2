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
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs = match_ast(graph, args.n_id, "switch_label")
    case_id = childs.get("switch_label")

    if case_id:
        case_expr = node_to_str(graph, case_id)
    else:
        case_expr = "Default"

    execution_ids = [
        _id
        for _id in adj_ast(graph, args.n_id)
        if graph.nodes[_id]["label_type"] in JAVA_STATEMENT
        and graph.nodes[_id]["label_type"] != "break_statement"
    ]

    return build_switch_section_node(args, case_expr, execution_ids)
