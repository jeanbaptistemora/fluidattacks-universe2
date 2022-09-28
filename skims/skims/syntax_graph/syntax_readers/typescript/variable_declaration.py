# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    TYPESCRIPT_PRIMARY_TYPES,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:

    var_dec_id = match_ast_d(args.ast_graph, args.n_id, "variable_declarator")
    var_name = None

    if var_dec_id:
        type_anno = match_ast_d(args.ast_graph, var_dec_id, "type_annotation")
        match = match_ast(args.ast_graph, var_dec_id, "identifier")
        var_name = node_to_str(args.ast_graph, str(match["identifier"]))

        if type_anno:
            childs_id = adj_ast(
                args.ast_graph,
                type_anno,
            )

            valid_childs = [
                child
                for child in childs_id
                if args.ast_graph.nodes[child]["label_type"]
                in TYPESCRIPT_PRIMARY_TYPES
            ]

    return build_variable_declaration_node(
        args, var_name, None, None, valid_childs
    )
