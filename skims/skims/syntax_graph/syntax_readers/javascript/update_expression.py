# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.update_expression import (
    build_update_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = match_ast(args.ast_graph, args.n_id)

    if type_id := c_ids.get("__1__"):
        exp_type = args.ast_graph.nodes[type_id].get("label_text")
    else:
        exp_type = "UpdateExpression"

    ident_id = c_ids.get("__0__")

    return build_update_expression_node(args, exp_type, ident_id)
