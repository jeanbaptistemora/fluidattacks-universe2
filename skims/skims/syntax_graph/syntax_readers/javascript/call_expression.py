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
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    call_node = args.ast_graph.nodes[args.n_id]
    method_id = call_node["label_field_function"]
    expr = node_to_str(args.ast_graph, method_id)
    args_id = call_node["label_field_arguments"]
    return build_method_invocation_node(args, expr, method_id, args_id, None)
