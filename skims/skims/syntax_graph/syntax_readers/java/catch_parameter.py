# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.catch_parameter import (
    build_catch_parameter_node,
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
    graph = args.ast_graph
    cp_node = graph.nodes[args.n_id]
    identifier_id = cp_node["label_field_name"]
    identifier = node_to_str(graph, identifier_id)
    catch_type = match_ast_d(graph, args.n_id, "catch_type")

    return build_catch_parameter_node(args, identifier, catch_type)
