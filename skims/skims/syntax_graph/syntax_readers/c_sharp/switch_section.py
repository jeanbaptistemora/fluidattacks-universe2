# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    C_SHARP_STATEMENT,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    execution_ids = [
        _id
        for _id in adj_ast(graph, args.n_id)
        if graph.nodes[_id]["label_type"] in C_SHARP_STATEMENT
    ]

    return build_switch_section_node(args, None, execution_ids)
