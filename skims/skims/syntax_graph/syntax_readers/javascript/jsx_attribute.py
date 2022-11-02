# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs = match_ast(graph, args.n_id, "=")
    if var_id := childs.get("__0__"):
        var_name = node_to_str(graph, var_id)
    else:
        var_name = "UnnamedVar"

    value_id = childs.get("__1__")

    if value_id and graph.nodes[value_id]["label_type"] == "jsx_expression":
        value_id = match_ast(graph, value_id, "{").get("__0__")

    return build_variable_declaration_node(args, var_name, None, value_id)
