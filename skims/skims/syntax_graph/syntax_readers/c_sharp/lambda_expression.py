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


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(
        args.ast_graph,
        args.n_id,
        "parameter_list",
        "identifier",
        "block",
        "invocation_expression",
    )
    var_name = match_childs.get("identifier")
    parameters = match_childs.get("parameter_list")
    block_node = match_childs.get("block")
    invocation_exp = match_childs.get("invocation_expression")
    return build_lambda_expression_node(
        args, var_name, parameters, block_node, invocation_exp
    )
