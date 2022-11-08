# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
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
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)

    if (
        len(c_ids) == 3
        and (selector_id := match_ast_d(graph, args.n_id, "selector"))
        and (arg_id := match_ast_d(graph, selector_id, "argument_part"))
    ):
        expr = node_to_str(graph, c_ids[0])
        args_id = match_ast_d(graph, arg_id, "arguments")
        return build_method_invocation_node(
            args, expr, c_ids[0], args_id, None
        )

    return build_expression_statement_node(
        args,
        c_ids=(_id for _id in c_ids if graph.nodes[_id]["label_type"] != ";"),
    )
