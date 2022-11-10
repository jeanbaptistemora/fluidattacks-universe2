# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.initialized_identifier import (
    build_initialized_identifier_node,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)
    equalizer = match_ast_d(args.ast_graph, args.n_id, "=")

    if len(c_ids) == 3 and equalizer:
        var_name = node_to_str(args.ast_graph, c_ids[0])
        return build_variable_declaration_node(args, var_name, None, c_ids[2])

    ignored_types = {"="}
    filtered_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_types
    ]
    return build_initialized_identifier_node(args, iter(filtered_ids))
