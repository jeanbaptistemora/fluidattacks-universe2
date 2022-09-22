# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.export_statement import (
    build_export_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node = args.ast_graph.nodes[args.n_id]
    b_types = {
        "function_declaration",
        "class_declaration",
        "generator_function_declaration",
    }
    export_block = None
    expression = None
    value_id = node.get("label_field_declaration")

    if not value_id:
        expression = "ExportClause"
    elif args.ast_graph.nodes[value_id]["label_type"] in b_types:
        export_block = value_id
    else:
        expression = node_to_str(args.ast_graph, value_id)

    return build_export_statement_node(args, expression, export_block)
