# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.lambda_expression import (
    build_lambda_expression_node,
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
    n_attrs = args.ast_graph.nodes[args.n_id]
    body_id = n_attrs["label_field_body"]
    match_childs = match_ast(
        args.ast_graph,
        args.n_id,
        "parameter_list",
        "identifier",
    )
    var_id = match_childs.get("identifier")
    if var_id:
        identifier = node_to_str(args.ast_graph, var_id)
    else:
        identifier = "Unnamed"

    parameters_id = match_childs.get("parameter_list")

    return build_lambda_expression_node(
        args, identifier, body_id, parameters_id
    )
