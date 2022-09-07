# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.call_expression import (
    build_call_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    call_node = args.ast_graph.nodes[args.n_id]
    function_id = call_node["label_field_function"]
    args_id = call_node["label_field_arguments"]
    fn_name = node_to_str(args.ast_graph, function_id)
    return build_call_expression_node(args, fn_name, args_id)
