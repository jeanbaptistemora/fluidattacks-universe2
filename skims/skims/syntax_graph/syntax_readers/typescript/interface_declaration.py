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
    get_ast_childs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    name = node_to_str(args.ast_graph, name_id)
    body_id = args.ast_graph.nodes[args.n_id]["label_field_body"]
    clause = get_ast_childs(args.ast_graph, args.n_id, "extends_clause")
    var_type = None
    if clause:
        var_type = node_to_str(args.ast_graph, clause[0]).replace(
            "extends", ""
        )
    return build_variable_declaration_node(args, name, var_type, body_id)
