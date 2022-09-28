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
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:

    var_decl_id = match_ast_d(args.ast_graph, args.n_id, "variable_declarator")

    var = None
    if var_decl_id:
        match = match_ast(args.ast_graph, var_decl_id, "identifier")
        var = node_to_str(args.ast_graph, str(match["identifier"]))

    return build_variable_declaration_node(args, var, None, None, var_decl_id)
