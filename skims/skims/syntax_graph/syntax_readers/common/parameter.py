# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShardMetadataLanguage,
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Iterator,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    param_node = graph.nodes[args.n_id]

    type_id = param_node.get("label_field_type")
    var_type = node_to_str(graph, type_id) if type_id else None

    identifier_id = param_node.get("label_field_name")
    var_name = node_to_str(graph, identifier_id) if identifier_id else None

    if args.language == GraphShardMetadataLanguage.DART:
        c_ids = adj_ast(graph, args.n_id)
    elif args.language == GraphShardMetadataLanguage.JAVA:
        c_ids = tuple(match_ast_group_d(graph, args.n_id, "modifiers"))
    else:
        c_ids = ()

    return build_parameter_node(
        args, var_name, var_type, cast(Iterator[str], c_ids)
    )
