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
    fn_name = node_to_str(args.ast_graph, function_id)

    func_type = args.ast_graph.nodes[function_id]["label_type"]
    if func_type not in {"member_expression", "call_expression"}:
        function_id = None

    args_id = call_node["label_field_arguments"]
    return build_call_expression_node(args, fn_name, function_id, args_id)
