# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
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
    arguments_id = args.ast_graph.nodes[args.n_id]["label_field_arguments"]
    expr_id = args.ast_graph.nodes[args.n_id]["label_field_function"]
    expr = node_to_str(args.ast_graph, expr_id)

    if "__0__" not in match_ast(args.ast_graph, arguments_id, "(", ")"):
        arguments_id = None

    return build_method_invocation_node(
        args, expr, expr_id, arguments_id, None
    )
